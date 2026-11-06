# Pocket Polyglot 🗺️

Skill para o Claude montar **programas de estudo de idiomas ultra-personalizados** — para qualquer idioma — e entregar um **roteiro interativo em HTML**, semana a semana, com checklist e porcentagem de progresso.

## Inspiração

Esta skill nasceu dos prompts mostrados no vídeo **"Learning ENGLISH has NEVER been this EASY"**, do canal Luis Mota:
▶️ https://www.youtube.com/watch?v=nVlM7IYEHvE

Os prompts originais criavam um plano de inglês com base em Natural Method e Comprehensible Input e depois o transformavam em um roteiro HTML. A skill generaliza a ideia para qualquer idioma, adiciona teste de nivelamento CEFR, definição automática do nível-alvo a partir do objetivo, estimativa de prazo com premissas explícitas e um template HTML padronizado.

## Como funciona

```
1. Entrevista        →  idioma, objetivo, minutos/dia, dias da semana, interesses, dificuldade
2. Nível atual       →  teste de nivelamento (recomendado) | nível CEFR informado | pular
3. Nível-alvo        →  sugerido a partir do objetivo (ex.: reuniões de trabalho → B2)
4. Estimativa        →  horas necessárias e prazo em faixa (otimista / conservador)
5. Diagnóstico       →  estratégia, semana-tipo, recursos, como medir progresso
6. Roteiro HTML      →  ciclo de 8 semanas com tema, gramática, 70–100 itens de vocabulário,
                         recursos e atividade de cada dia; checklist e % de progresso
```

### O teste de nivelamento é opcional
A skill explica por que o teste deixa o plano mais assertivo (o input precisa ser *compreensível* para funcionar), mas a decisão é do usuário. Quem preferir pode informar o próprio nível CEFR ou descrever o que consegue fazer — o plano é gerado de qualquer forma.

O teste é adaptativo (sobe ou desce de nível conforme as respostas), dura ~15–25 min e cobre vocabulário/gramática, leitura, escrita e, opcionalmente, compreensão oral e fala. O resultado traz o nível global, o nível por habilidade e o grau de confiança.

> ⚠️ **Importante:** o nível indicado pelo teste é apenas uma **estimativa gerada por IA** e **não substitui uma avaliação real de proficiência conforme o CEFR**. O teste tem poucos itens, não é padronizado como os exames oficiais, não conta com avaliador humano e, sem áudio, avalia pouco a compreensão oral e a fala. Use-o para calibrar o plano de estudos, não como comprovação de nível em currículo, vaga, intercâmbio ou visto. Para isso, procure exames reconhecidos (ex.: Cambridge, IELTS, TOEFL para inglês; DELE/SIELE para espanhol; DELF/DALF para francês; Goethe-Zertifikat para alemão). O roteiro HTML também exibe esse aviso quando o nível veio do teste.

### Metodologia
O eixo é **Comprehensible Input** (Krashen) e **Método Natural**, com quatro frentes:

- **Imersão em tempos mortos** — trajeto, academia, tarefas de casa; dispositivos no idioma-alvo; treino ativo do algoritmo das redes sociais.
- **Barril de Conteúdos** — pastas pré-selecionadas (fácil / no ponto / desafio / já usado) para não perder tempo escolhendo o que estudar.
- **Micro-hábitos** — pensar no idioma, falar sozinho, pesquisa relâmpago de objetos e ações ao redor.
- **Imersão ativa** — shadowing, chorusing, sentence mining, flashcards (SRS), leitura e escrita com correção por IA, interação com conteúdo já visto e roleplay de situações reais.

A skill não é "só input": a pesquisa (Swain, Long, meta-análises sobre instrução explícita) mostra que produção, interação, feedback e um pouco de gramática explícita também aceleram o aprendizado. Por isso a proporção entre input e produção muda conforme o nível.

### Estimativa de prazo
Usa as horas guiadas cumulativas da Cambridge English por nível CEFR, ajustadas pela distância entre a língua nativa e a língua-alvo, e conta a imersão passiva com peso parcial. O resultado é sempre uma faixa com as premissas declaradas — e, se o prazo do usuário não fechar com a conta, a skill avisa.

### O roteiro HTML
- Barra de progresso geral no topo (dias concluídos ÷ dias de estudo).
- Semanas em acordeão; clicar em um dia abre o que estudar, em qual recurso e por quantos minutos.
- Checkbox "Dia concluído"; o progresso fica salvo no navegador, com botões para exportar/importar.
- Vocabulário com filtro e botão para copiar no formato do Anki (TSV).
- **Checkpoints de gravação** (início, meio e fim do ciclo) para comparar a fala com critérios simples.
- Funciona no celular e em modo escuro.

O roteiro é gerado em **ciclos de 8 semanas**: depois disso o nível já mudou, e o próximo ciclo deve ser recalibrado (de preferência com um re-teste).

**Vocabulário semana a semana.** As 2 primeiras semanas já vêm com a lista completa (70–100 itens). Nas seguintes, o roteiro mostra os campos de vocabulário da semana; quando o usuário chega lá, pede *"vocabulário da semana 3"* ao Claude e cola a lista no próprio roteiro. Assim a lista se ajusta ao que ele realmente aprendeu, e o plano inicial fica bem mais leve de gerar.

### Economia de uso
A skill foi desenhada para funcionar bem com limites de uso apertados, sem entregar menos para ninguém:
- **Entrevista em uma única mensagem** e teste de nivelamento em ~5 mensagens.
- **Semana-modelo:** os dias são descritos uma vez e cada semana só informa o que muda (episódio, tema da escrita, cenário do roleplay).
- **Vocabulário sob demanda** a partir da semana 3, em formato compacto (`termo | tradução | exemplo`).
- **Sem repetição:** o chat traz um resumo; o detalhe dia a dia fica no roteiro.
- **Referências lidas só na etapa em que são necessárias** e no máximo 3–4 buscas na web.
- O script valida o plano antes de gerar o HTML, evitando idas e vindas para corrigir erros.

## Estrutura

```
pocket-polyglot/
├── SKILL.md                       # instruções principais (fluxo da skill)
├── README.md
├── references/
│   ├── cefr.md                    # níveis, objetivo → nível, horas, estimativa de prazo
│   ├── teste-nivelamento.md       # roteiro do teste adaptativo
│   ├── metodologia.md             # técnicas, proporções por nível, evidências
│   ├── recursos.md                # recursos conhecidos por idioma
│   └── formato-do-plano.md        # formato do JSON do roteiro
├── assets/
│   ├── roteiro_template.html      # template interativo
│   └── exemplo_plano.json         # exemplo completo no formato atual
└── scripts/
    └── build_roadmap.py           # valida o JSON e gera o HTML
```

Gerar um roteiro manualmente:
```bash
python scripts/build_roadmap.py meu_plano.json roteiro.html
```

## Como usar

Basta pedir ao Claude algo como:
- "Quero aprender inglês para reuniões de trabalho, tenho 30 minutos por dia."
- "Monta um plano de espanhol pra eu viajar em março."
- "Qual é meu nível de francês? Quero fazer um teste."

## Fontes
- Cambridge English — Guided learning hours: https://support.cambridgeenglish.org/hc/en-gb/articles/202838506-Guided-learning-hours
- Conselho da Europa — Common European Framework of Reference for Languages (CEFR)
- Krashen, S. (1982). *Principles and Practice in Second Language Acquisition*; Krashen & Terrell (1983). *The Natural Approach*
- Swain, M. (1985) — Output Hypothesis; Long, M. (1996) — Interaction Hypothesis
- Norris, J. & Ortega, L. (2000). Effectiveness of L2 instruction: a research synthesis and quantitative meta-analysis
- Milton, J. (2010) — tamanho de vocabulário por nível CEFR
