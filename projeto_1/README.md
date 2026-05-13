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

Comandos uteis para manter a qualidade de codigo durante o desenvolvimento.

```bash
# mostra os comandos disponiveis
just

# exemplo
just test  # roda testes
just test -k some_test  # -k filtra por nomer. No caso: 'some_test'
just format
```
