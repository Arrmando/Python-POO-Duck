# Projeto 1

\<Incluir aqui uma descricao curta sobre o que é o projeto>

Veja a documentação completa em [aqui](docs/).

## Desenvolvimento

### Requisitos

Primeiramente, instalar os seguintes programas (compativel com windows e linux).

- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

### Teste manual

Um modulo pode ser executado diretamente para testes simples.
Coloque a parte executado do código em um `if __name__ == "__main__"` para evitar execuções indesejadas desse código de teste.
Então rode (subsitua `projeto_1.main` pelo módulo desejado):

```bash
# O arquivo 'src/projeto_1/main.py' representa o modulo projeto_1.main
uv run python -m projeto_1.main
```

### Comandos

Comandos úteis para manter a qualidade de código durante o desenvolvimento (requer `just`).

```bash
# Mostra os comandos disponíveis
just

# Exemplo
just test             # Roda testes
just test -k pattern  # Filtra testes por nome
just format           # Formata o código
```

### Testes (sem uv/just)

Para configurar o ambiente virtual e rodar os testes utilizando apenas `python` e `venv`:

**1. Configuração do ambiente:**

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
source .venv/bin/activate  # (linux/mac)
.venv\Scripts\activate  # (windows)

# Instalar dependências de desenvolvimento
pip install --group dev -e .
```

**2. Execução dos testes:**

```bash
# Rodar todos os testes
python -m pytest

# Rodar testes filtrando por nome (ex: apenas testes que contenham 'ingrediente')
python -m pytest -k ingrediente
```

**3. Formatação do código:**

```bash
# Formatar o código
ruff format .
ruff check --fix .
```
