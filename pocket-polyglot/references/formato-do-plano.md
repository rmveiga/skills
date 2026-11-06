# Formato do JSON do roteiro

`scripts/build_roadmap.py` lê este JSON e gera o HTML a partir de `assets/roteiro_template.html`. Exemplo completo e válido em `assets/exemplo_plano.json`.

## Campos do topo

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | sim | Único por plano/ciclo (ex.: `"ingles-ana-ciclo1"`). É a chave do progresso salvo no navegador. |
| `titulo`, `idioma_alvo` | sim | |
| `nivel_atual`, `nivel_alvo` | sim | Ex.: `"B1"`, `"B2"`. |
| `nivel_origem` | sim | `"teste_ia"`, `"certificado"` ou `"autodeclarado"`. Com `teste_ia`, o HTML mostra o aviso de que o nível é estimativa por IA e não substitui avaliação real conforme o CEFR. |
| `objetivo`, `estimativa` | sim | Textos curtos. |
| `minutos_por_dia` | sim | Os blocos de cada dia de estudo devem somar isso. |
| `dias_estudo` | sim | Códigos `seg ter qua qui sex sab dom`. Os demais dias aparecem como imersão passiva. |
| `ciclo` | não | Número do ciclo. |
| `vocab_minimo` | não | Padrão 70. Use 40 para quem estuda menos de 30 min/dia. |
| `vocab_semanas_completas` | não | Padrão 2. Quantas semanas iniciais trazem o vocabulário completo embutido. |
| `rotina_passiva` | não | `[{"momento": "...", "conteudo": "..."}]` — tempos mortos. |
| `micro_habitos` | não | Lista de textos. |
| `semana_tipo` | recomendado | Modelo de dias (ver abaixo). |

## Semana-modelo

Defina os dias uma única vez. Os textos de `foco`, `atividade`, `recurso` e `instrucoes` aceitam marcadores: `{tema}` e `{gramatica}` são preenchidos automaticamente; qualquer outro (`{input}`, `{escrita}`, `{roleplay}`…) vem de `tarefas` de cada semana.

```json
"semana_tipo": {
  "seg": {"foco": "Input + vocabulário", "blocos": [
    {"atividade": "Escuta ativa", "recurso": "{input}", "minutos": 15, "instrucoes": "Ouvir 1x sem transcrição, depois com; minerar 5 frases sobre {tema}."},
    {"atividade": "Flashcards", "recurso": "Anki", "minutos": 15, "instrucoes": "Revisões + até 12 cartões novos."}
  ]},
  "ter": {"foco": "Escrita", "blocos": [
    {"atividade": "Escrita com IA", "recurso": "Claude", "minutos": 30, "instrucoes": "{escrita} Pedir correção explicada."}
  ]}
}
```

## Semanas

```json
{
  "numero": 1,
  "tema": "Apresentando-se no trabalho",
  "objetivo_semana": "Falar 2 minutos sobre você e sua função",
  "gramatica": {"topico": "Present simple vs. present continuous", "explicacao": "…", "exemplos": ["…", "…"]},
  "tarefas": {"input": "6 Minute English — episódio sobre trabalho", "escrita": "Escreva 100 palavras…", "roleplay": "…"},
  "vocabulario": ["to be in charge of | ser responsável por | I'm in charge of regression tests."],
  "vocab_foco": ["status e progresso", "bloqueios e riscos"],
  "recursos": [{"nome": "BBC Learning English", "tipo": "podcast", "url": "https://…", "como_usar": "…"}],
  "micro_habito": "…",
  "checkpoint": {"titulo": "Gravação de base", "tarefa": "Grave 2 min respondendo…", "criterios": ["Fluência", "Precisão", "Conteúdo", "Recuperação quando trava"]},
  "substituir_dias": {"sex": {"foco": "Simulação", "blocos": [{"atividade": "…", "recurso": "…", "minutos": 30, "instrucoes": "…"}]}}
}
```

- `vocabulario`: obrigatório nas semanas até `vocab_semanas_completas`; nas demais, deixe vazio e preencha `vocab_foco` (3–6 campos). O usuário cola a lista depois no próprio roteiro.
- Formato compacto do vocabulário: `"termo | tradução | exemplo"`. O formato objeto `{"termo","traducao","exemplo"}` também é aceito, mas gasta mais texto.
- `dias` explícitos (lista com `dia`, `foco`, `blocos`) continuam aceitos e substituem a semana-modelo naquela semana — use só se a semana inteira fugir do padrão.
- `url` é opcional; só inclua links verificados.

## O que o script verifica

Campos obrigatórios; dias de estudo presentes; soma de minutos por dia; marcadores sem valor em `tarefas`; vocabulário mínimo nas semanas completas; `vocab_foco` nas demais; termos repetidos dentro e entre semanas; `nivel_origem` válido.
