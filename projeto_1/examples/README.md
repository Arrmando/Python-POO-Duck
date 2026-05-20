# Exemplos de uso da API

Suba o servidor:

```bash
just up
```

## GET /insumo

```bash
curl http://localhost:8000/insumo 2>/dev/null | jq
```

## POST /insumo

```bash
curl -X POST http://localhost:8000/insumo \
  -H "Content-Type: application/json" \
  -d @post_ingrediente.json 2>/dev/null | jq
```

Os arquivos `.json` neste diretório contêm payloads prontos para uso.
Execute o comando acima substituindo o nome do arquivo pelo desejado.
