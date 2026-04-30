# Projeto 1

\<Incluir aqui uma descricao curta sobre o que é o projeto>

Veja a documentação completa em [aqui](docs/).

## Desenvolvimento

### Requisitos

Primeiramente, instalar os seguintes programas.
Compativel com windows e linux.

- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

### Teste manual

Rodar modulos diretamente.
O modulo pode ter um main() para testes simples.

```bash
uv run python -m projeto_1.main
```

### Comandos

Comandos uteis para manter a qualidade de codigo durante o desenvolvimento.

```bash
# mostra os comandos disponiveis
just

# exemplo
just test  # roda tests
just test -k some_test  # -k filtra por nomer. No caso: 'some_test'
just test -vk some_test  # -v para modo verboso
just test -svk some_test  # -s para mostrar saidas de print
```
