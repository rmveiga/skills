#!/usr/bin/env python3
"""Gera o roteiro HTML interativo a partir do JSON do plano.

Uso:
    python scripts/build_roadmap.py plano.json roteiro.html [--template caminho]

Valida o plano (dias, minutos, vocabulário) e imprime avisos. Sai com código 1
se houver erro estrutural; avisos não impedem a geração.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DIAS_VALIDOS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PADRAO = SKILL_DIR / "assets" / "roteiro_template.html"


def vocab_item(v):
    """Aceita objeto {termo, traducao, exemplo} ou string compacta 'termo | tradução | exemplo'."""
    if isinstance(v, str):
        p = [x.strip() for x in re.split(r"[|\t]", v)]
        return {"termo": p[0], "traducao": p[1] if len(p) > 1 else "", "exemplo": p[2] if len(p) > 2 else ""}
    return {"termo": str(v.get("termo", "")), "traducao": v.get("traducao", ""), "exemplo": v.get("exemplo", "")}


def validar(plano):
    erros, avisos = [], []
    for campo in ("titulo", "idioma_alvo", "dias_estudo", "semanas"):
        if not plano.get(campo):
            erros.append(f"Campo obrigatório ausente: '{campo}'")
    if erros:
        return erros, avisos

    dias = plano["dias_estudo"]
    invalidos = [d for d in dias if d not in DIAS_VALIDOS]
    if invalidos:
        erros.append(f"dias_estudo com códigos inválidos {invalidos}; use {DIAS_VALIDOS}")
    if not plano.get("id"):
        avisos.append("Sem 'id': o progresso salvo usará o título como chave. Defina um id único por plano/ciclo.")

    if plano.get("nivel_origem") not in ("teste_ia", "certificado", "autodeclarado"):
        avisos.append("'nivel_origem' ausente ou inválido (use teste_ia, certificado ou autodeclarado); sem ele o HTML não mostra o aviso de estimativa por IA.")

    minutos = plano.get("minutos_por_dia")
    vocab_min = plano.get("vocab_minimo", 70)
    vocab_completas = plano.get("vocab_semanas_completas", 2)
    modelo = plano.get("semana_tipo") or {}

    for d, t in modelo.items():
        if d not in DIAS_VALIDOS:
            erros.append(f"semana_tipo: dia inválido '{d}'")
        total = sum(int(b.get("minutos") or 0) for b in t.get("blocos") or [])
        if minutos and total != minutos:
            avisos.append(f"semana_tipo/{d}: blocos somam {total} min (esperado {minutos})")

    numeros = []
    for i, s in enumerate(plano["semanas"], 1):
        n = s.get("numero", i)
        numeros.append(n)
        rot = f"Semana {n}"
        if not s.get("tema"):
            erros.append(f"{rot}: sem 'tema'")
        if not (s.get("gramatica") or {}).get("topico"):
            avisos.append(f"{rot}: sem tópico gramatical")
        voc = [vocab_item(v) for v in s.get("vocabulario") or []]
        if i <= vocab_completas:
            if len(voc) < vocab_min:
                avisos.append(f"{rot}: {len(voc)} itens de vocabulário (mínimo configurado: {vocab_min})")
        elif not voc and len(s.get("vocab_foco") or []) < 3:
            avisos.append(f"{rot}: sem vocabulário e sem 'vocab_foco' (liste ao menos 3 campos de vocabulário para orientar a geração sob demanda)")
        termos = [v["termo"].strip().lower() for v in voc]
        dup = sorted({t for t in termos if t and termos.count(t) > 1})
        if dup:
            avisos.append(f"{rot}: vocabulário repetido: {', '.join(dup[:10])}")
        if not s.get("recursos"):
            avisos.append(f"{rot}: sem recursos")
        if not s.get("dias") and not modelo:
            erros.append(f"{rot}: sem 'dias' e o plano não tem 'semana_tipo'")
            continue
        por_dia = {d: modelo[d] for d in modelo}
        por_dia.update({d.get("dia"): d for d in s.get("dias") or []})
        por_dia.update(s.get("substituir_dias") or {})
        tarefas = s.get("tarefas") or {}
        for d in dias:
            if d not in por_dia:
                erros.append(f"{rot}: falta o dia de estudo '{d}'")
                continue
            blocos = por_dia[d].get("blocos") or []
            if not blocos:
                erros.append(f"{rot}/{d}: sem blocos de atividade")
            total = sum(int(b.get("minutos") or 0) for b in blocos)
            if minutos and total != minutos:
                avisos.append(f"{rot}/{d}: blocos somam {total} min (esperado {minutos})")
            textos = " ".join(str(b.get(k, "")) for b in blocos for k in ("atividade", "recurso", "instrucoes")) + str(por_dia[d].get("foco", ""))
            faltando = sorted({k for k in re.findall(r"\{(\w+)\}", textos) if k not in ("tema", "gramatica") and k not in tarefas})
            if faltando:
                avisos.append(f"{rot}/{d}: marcadores sem valor em 'tarefas': {faltando}")
        extras = [d for d in por_dia if d not in dias]
        if extras:
            avisos.append(f"{rot}: dias fora de dias_estudo serão exibidos como imersão passiva: {extras}")
    if len(set(numeros)) != len(numeros):
        erros.append("Números de semana repetidos")

    vistos = {}
    for s in plano["semanas"]:
        for v in s.get("vocabulario") or []:
            t = vocab_item(v)["termo"].strip().lower()
            if t:
                vistos.setdefault(t, set()).add(s.get("numero"))
    cruzados = [t for t, ws in vistos.items() if len(ws) > 1]
    if cruzados:
        avisos.append(f"{len(cruzados)} termos aparecem em mais de uma semana (ex.: {', '.join(cruzados[:8])})")
    return erros, avisos

    dias = plano["dias_estudo"]
    invalidos = [d for d in dias if d not in DIAS_VALIDOS]
    if invalidos:
        erros.append(f"dias_estudo com códigos inválidos {invalidos}; use {DIAS_VALIDOS}")
    if not plano.get("id"):
        avisos.append("Sem 'id': o progresso salvo usará o título como chave. Defina um id único por plano/ciclo.")

    if plano.get("nivel_origem") not in ("teste_ia", "certificado", "autodeclarado"):
        avisos.append("'nivel_origem' ausente ou inválido (use teste_ia, certificado ou autodeclarado); sem ele o HTML não mostra o aviso de estimativa por IA.")

    minutos = plano.get("minutos_por_dia")
    vocab_min = plano.get("vocab_minimo", 70)

    numeros = []
    for i, s in enumerate(plano["semanas"], 1):
        n = s.get("numero", i)
        numeros.append(n)
        rot = f"Semana {n}"
        if not s.get("tema"):
            erros.append(f"{rot}: sem 'tema'")
        if not (s.get("gramatica") or {}).get("topico"):
            avisos.append(f"{rot}: sem tópico gramatical")
        voc = s.get("vocabulario") or []
        if len(voc) < vocab_min:
            avisos.append(f"{rot}: {len(voc)} itens de vocabulário (mínimo configurado: {vocab_min})")
        termos = [str(v.get("termo", "")).strip().lower() for v in voc]
        dup = sorted({t for t in termos if t and termos.count(t) > 1})
        if dup:
            avisos.append(f"{rot}: vocabulário repetido: {', '.join(dup[:10])}")
        if not s.get("recursos"):
            avisos.append(f"{rot}: sem recursos")
        por_dia = {d.get("dia"): d for d in s.get("dias") or []}
        for d in dias:
            if d not in por_dia:
                erros.append(f"{rot}: falta o dia de estudo '{d}'")
                continue
            blocos = por_dia[d].get("blocos") or []
            if not blocos:
                erros.append(f"{rot}/{d}: sem blocos de atividade")
            total = sum(int(b.get("minutos") or 0) for b in blocos)
            if minutos and total != minutos:
                avisos.append(f"{rot}/{d}: blocos somam {total} min (esperado {minutos})")
        extras = [d for d in por_dia if d not in dias]
        if extras:
            avisos.append(f"{rot}: dias fora de dias_estudo serão exibidos como imersão passiva: {extras}")
    if len(set(numeros)) != len(numeros):
        erros.append("Números de semana repetidos")

    # vocabulário repetido entre semanas
    vistos = {}
    for s in plano["semanas"]:
        for v in s.get("vocabulario") or []:
            t = str(v.get("termo", "")).strip().lower()
            if t:
                vistos.setdefault(t, set()).add(s.get("numero"))
    cruzados = [t for t, ws in vistos.items() if len(ws) > 1]
    if cruzados:
        avisos.append(f"{len(cruzados)} termos aparecem em mais de uma semana (ex.: {', '.join(cruzados[:8])})")
    return erros, avisos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plano")
    ap.add_argument("saida")
    ap.add_argument("--template", default=str(TEMPLATE_PADRAO))
    a = ap.parse_args()

    try:
        plano = json.loads(Path(a.plano).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERRO: JSON inválido em {a.plano}: {e}")
        sys.exit(1)

    erros, avisos = validar(plano)
    for w in avisos:
        print(f"AVISO: {w}")
    for e in erros:
        print(f"ERRO: {e}")
    if erros:
        sys.exit(1)

    tpl = Path(a.template).read_text(encoding="utf-8")
    if "__PLAN_JSON__" not in tpl:
        print("ERRO: template sem o marcador __PLAN_JSON__")
        sys.exit(1)
    dados = json.dumps(plano, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("__PLAN_JSON__", dados)
    if plano.get("titulo"):
        titulo = plano["titulo"].replace("&", "&amp;").replace("<", "&lt;")
        html = html.replace("<title>Pocket Polyglot</title>", f"<title>{titulo}</title>", 1)
    Path(a.saida).write_text(html, encoding="utf-8")

    n_sem = len(plano["semanas"])
    n_voc = sum(len(s.get("vocabulario") or []) for s in plano["semanas"])
    tamanho = Path(a.plano).stat().st_size
    print(f"OK: {a.saida} gerado — {n_sem} semanas, {n_sem * len(plano['dias_estudo'])} dias de estudo, {n_voc} itens de vocabulário embutidos, plano com {tamanho // 1024} KB, {len(avisos)} aviso(s).")


if __name__ == "__main__":
    main()
