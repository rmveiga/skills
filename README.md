# Skills para IA

Coleção de **skills para o Claude** criadas e mantidas por Rafael Morán.

Uma *skill* é uma pasta com instruções (`SKILL.md`) e, opcionalmente, referências, templates e scripts que ensinam o Claude a executar um tipo de tarefa de forma consistente. Quando um pedido corresponde à descrição da skill, o Claude a carrega e segue o fluxo definido nela, em vez de responder de forma genérica.

O objetivo deste repositório é reunir skills úteis para o dia a dia, testadas na prática e documentadas, para que qualquer pessoa possa instalá-las, usá-las e adaptá-las.

## Índice de skills

| Skill | Descrição |
|-------|-----------|
| [pocket-polyglot](./pocket-polyglot/) | Monta programas de estudo de idiomas personalizados, com teste de nivelamento CEFR opcional, e entrega um roteiro interativo em HTML semana a semana. |

Cada skill tem seu próprio `README.md` com detalhes de funcionamento, metodologia e exemplos de uso.

## Estrutura do repositório

```
skills/
├── README.md              # este arquivo
├── LICENSE
└── <nome-da-skill>/
    ├── SKILL.md           # instruções principais (obrigatório)
    ├── README.md          # documentação para pessoas
    ├── references/        # material consultado pela skill sob demanda
    ├── assets/            # templates e exemplos
    └── scripts/           # scripts auxiliares
```

Apenas o `SKILL.md` é obrigatório; as demais pastas existem conforme a necessidade de cada skill.

## Como usar

1. Baixe ou clone este repositório:
   ```bash
   git clone https://github.com/rmveiga/skills.git
   ```
2. Escolha a pasta da skill desejada e instale-a no ambiente em que você usa o Claude:
   - **Claude (app/web):** compacte a pasta da skill em `.zip` e envie-a na área de Skills das configurações.
   - **Claude Code:** copie a pasta da skill para `~/.claude/skills/` (uso pessoal) ou para `.claude/skills/` dentro do projeto.
3. Faça um pedido relacionado ao tema da skill. Não é preciso chamá-la pelo nome: o Claude a aciona a partir da descrição.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](./LICENSE).
