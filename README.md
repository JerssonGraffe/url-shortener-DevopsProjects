# URL Shortener — aplicação e deploy

Projeto pessoal de portfólio DevOps: aplicação Python 3.13 com **FastAPI + Mangum**, empacotada como imagem para AWS Lambda. O [repositório de infraestrutura](https://github.com/JerssonGraffe/infraestruture-DevopsProjects) define API Gateway, Lambda, DynamoDB, IAM e ECR com Terraform.

## Como funciona

| Rota | Comportamento |
| --- | --- |
| `GET /` | Retorna `{"status": "ok"}` |
| `POST /shorten` | Recebe `{"url": "https://exemplo.com"}`, solicita um link ao TinyURL e salva `short_code`, URLs original/curta e data de criação no DynamoDB |

A resposta de `/shorten` contém `short_code`, `short_url` e `original_url`. O encurtamento é feito pelo **TinyURL**; este código não implementa uma rota própria de redirecionamento.

## Pipeline de deploy

Em cada push para `main`, [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

1. Autentica na AWS usando os secrets `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` e faz login no ECR.
2. Constrói a imagem com Docker multi-stage: `uv` instala as dependências no builder Python 3.13; a imagem final usa Python 3.13-slim e `awslambdaric`.
3. Publica a tag `latest` no ECR `url-shortener` e atualiza a função Lambda `url-shortener` para usá-la.

A infraestrutura e a imagem inicial precisam existir antes do primeiro deploy. O build também recebe uma tag local baseada no commit, mas o workflow publica somente `latest`.

## Executar localmente

Com [`uv`](https://docs.astral.sh/uv/) e Python 3.13:

```bash
uv sync --python 3.13 --frozen
uv run --python 3.13 --with uvicorn uvicorn entrypoints.app:app --reload
```

Para usar `POST /shorten`, são necessários acesso ao TinyURL e credenciais AWS com permissão de escrita na tabela `url-shortener-table`. O pipeline deste repositório é de **build e deploy**; ele não executa testes ou lint.
