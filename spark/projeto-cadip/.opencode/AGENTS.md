# projeto-cadip — AGENTS.md

ETL com PySpark para extração de dados do sistema CADIP, executado como AWS Glue Job.

## Setup

```bash
# Ativar virtual environment (raiz do monorepo)
source ../../venv/bin/activate       # bash
# source ../../venv/bin/activate.fish  # fish shell

# Java 17 (obrigatório para PySpark) — configurado via asdf
export JAVA_HOME=$HOME/.asdf/installs/java/openjdk-17.0.2

# Python 3.12 (asdf) — ver ../.tool-versions
pip install -r app/requirements.txt   # pyspark 4.1.2, awsglue3-local, mypy
```

## Comandos

| Comando | Onde executar | Descrição |
|---|---|---|
| `PYTHONPATH=app python app/run_local.py` | `spark/projeto-cadip/` | Modo local com dados fake (JSON) |
| `PYTHONPATH=app python app/main.py --JOB_NAME x --DATABASE_NAME y --TABLE_NAME z --ENVIRONMENT PROD` | `spark/projeto-cadip/` | Modo AWS Glue (real) |
| `mypy -p src` | `spark/projeto-cadip/` | Type checking (usa `mypy.ini`) |

`PYTHONPATH=app` é **obrigatório** para imports como `from src.service.*`.

## Arquitetura

- **Interface**: `app/src/extract.py:6` — `IExtract[T]` (ABC genérico)
- **Builder + Factory**: `app/src/etl/extract_builder.py:33` — `ExtractBuilder` → `RealExtractBuilder` / `FakeExtractBuilder`; `ExtractBuilderFactory:114` seleciona por ambiente
- **Config**: `app/src/service/glue_configuration.py:5` — `GlueConfiguration` container
- **Orquestrador**: `app/src/service/executor.py:5` — `Executor.run()` chama os 6 extracts
- **Domínios**: `app/src/domain/*.py` — cada classe wrappa um `DataFrame` e expõe `to_df()` com projeção tipada

### Ambiente vs Builder

| ENVIRONMENT | Builder usado | Fonte de dados |
|---|---|---|
| `LOCAL` | `FakeExtractBuilder` | JSONs em `app/src/*.json` |
| `DEV` / `HOM` / `PROD` | `RealExtractBuilder` | AWS Glue Data Catalog (`db_custodia/tb_*`) |

## Peculiaridades (agente, atenção!)

- **`main.py:run()` está desconectado** — `__main__` (linha 96) chama `run_job()` (leitura simples do catálogo), **não** `run()` (pipeline completo). O pipeline completo só funciona via `run_local.py` ou se você conectar manualmente.
- **Sem `__init__.py`** — `.gitignore` (raiz) ignora `*/__init__.py`. Não crie esses arquivos.
- **Database/table name**: cada extract real declara `__DATABASE_NAME` / `__TABLE_NAME` como constantes privadas de classe; construtor recebe apenas `glue_context`.
- **Todos os 6 real extracts implementados**: seguem o mesmo padrão com `__DATABASE_NAME`/`__TABLE_NAME` como constantes privadas de classe e `extract()` com `DynamicFrame.from_catalog`.
- **Typo em filename**: `app/src/indentificacao_pessoas.json` (falta "ta").
- **Transformação/relatórios descritos no README** (`DadosCadip`, `EntesPublicos`, `Transformer`, `IEvent`) **não estão implementados**.

## Testes

- `spark/testing_pyspark/` (projeto separado) usa `pyspark.testing.utils.assertDataFrameEqual` e `PySparkTestCase` (unittest)
- **projeto-cadip não tem testes**
