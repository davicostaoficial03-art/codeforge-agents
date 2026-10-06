# Construindo um orquestrador de agentes

Neste minicurso vamos construir, do zero, um sistema com **3 agentes de IA**
que trabalham juntos para gerar uma aplicação web a partir de um pedido em
linguagem natural:

```
Planner  →  gera o plano técnico
Coder    →  escreve o código
Reviewer →  revisa e aprova (ou manda corrigir)
```

O `Orchestrator` coordena esse ciclo: se o Reviewer reprovar, o Coder recebe
o feedback e tenta de novo, até `MAX_ITERATIONS` vezes.

## Pré-requisitos

- Python 3.10+
- Uma API key do Gemini ([aistudio.google.com](https://aistudio.google.com))

## Setup

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # e cole sua GEMINI_API_KEY
```

**Windows (PowerShell, terminal padrão do VS Code):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # e cole sua GEMINI_API_KEY
```

Se der erro de "execution policy" ao ativar, rode uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Passo 1 - A camada de LLM (`llm.py`)

Toda a comunicação com o Gemini passa por uma única função, `call_llm`.
Isso isola o resto do projeto de detalhes do SDK, se um dia você trocar de
provedor, só mexe aqui.

**Detalhe importante:** a partir da versão 2.18 do `google-genai`, o SDK
passou a logar o aviso abaixo em _toda_ chamada de `generate_content`,
mesmo sem usar `tools`:

```
Direct use of automatic function calling (AFC) in Models.generate_content
is not recommended...
```

É só um log informativo - não afeta o resultado. Para silenciá-lo sem mudar
nenhum comportamento, adicione isto antes de criar o client:

```python
import logging

logging.getLogger("google_genai.models").setLevel(logging.ERROR)
```

## Passo 2 - O que é um Agent (`agent.py`)

Um `Agent`, aqui, é só um nome + duas instruções carregadas de arquivos:
`AGENTS.md` (quem ele é / o que deve fazer) e `SKILL.md` (o que ele sabe
fazer). Isso separa **comportamento** de **conhecimento**, e permite editar
a "personalidade" de um agente sem tocar em código Python.

Cada agente vive em `agents/<nome>/`, com seu próprio `AGENTS.md` e
`SKILL.md`. Crie as pastas `agents/planner`, `agents/coder` e
`agents/reviewer` e escreva as instruções de cada um - pense em:

- **planner**: não escreve código, só decompõe o pedido em um plano;
- **coder**: escreve os arquivos, sempre no formato `FILE: nome\nconteúdo`;
- **reviewer**: só aprova/reprova, terminando com `APPROVED: YES` ou `APPROVED: NO`.

(As instruções completas usadas na demo estão em `agents/*/AGENTS.md` e
`agents/*/SKILL.md` neste repo, caso queira comparar depois de tentar.)

## Passo 3 - Tools: dando "mãos" ao Coder (`tools.py`)

O Coder devolve texto puro. Para virar arquivos de verdade no disco, alguém
precisa interpretar esse texto - essa é a parte mais "manual" do projeto
(sem tool calling nativo da API, é regex mesmo).

## Passo 4 - O Orchestrator

Este é o coração do projeto: um **loop de agente único orquestrando
outros agentes**. A cada iteração, o Coder recebe o plano + o código
anterior + a revisão anterior como contexto, assim ele sabe exatamente
o que corrigir.

## Passo 5 - `main.py`

Só amarra tudo: pergunta o pedido do usuário, chama o `Orchestrator` e
imprime o resultado.

```python
from orchestrator import Orchestrator


def main():
    request = input("Descreva a aplicação que você quer criar:\n\n> ")
    orchestrator = Orchestrator()
    result = orchestrator.run(request)
    print(f"Iterações: {result['iterations']}")
    print("Arquivos:", result["files"])


if __name__ == "__main__":
    main()
```

## Rodando

```bash
python main.py
python3 main.py
```

Os arquivos gerados aparecem em `generated_app/`.

## Estrutura final

```
codeforge/
├── agents/
│   ├── planner/{AGENTS.md, SKILL.md}
│   ├── coder/{AGENTS.md, SKILL.md}
│   └── reviewer/{AGENTS.md, SKILL.md}
├── agent.py
├── llm.py
├── tools.py
├── orchestrator.py
├── main.py
├── requirements.txt
└── .env
```
