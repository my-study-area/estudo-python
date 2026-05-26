# projeto-cadip

## Pré-requisitos
- python 12


## Configuração
```bash
pip install -r app/requirements.txt
```

Executa o projeto:
```bash
python app/main.py 
```


## Design de classes - 1
```
Contratos
Participantes
IdentificaoPessoas
DadosCadastrais(IdentificaoPessoas, Participantes)
  -> filterIdentificadorBy(Participantes) -> IdentificacaoEntesPublicos:
  -> filterParticipantesEnderecoPriorizado()
Tomadores
Garantidores
Ipocs
IdentificacaoEntesPublicos
ParticipantesEnderecoPriorizado
  __numero_contrato
  __id_pessoa
  __tipo_participante
  __municipio
  __uf
  to_df()

EntesPublicos(DadosCadastrais)
  __data_frame
  __participantes
  __participantes_enderecos_priorizados
  __identificao_pessoas
  __dados_cadastrais
  -> _join()
  -> _filter()
  -> identificador
  -> tomadores
  -> garantidores
  -> to_df()



Transformer(Contratos, IdentificacaoEntesPublicos)
  __data_frame
  __contratos_filtrados = filterBy(IdentificacaoEntesPublicos)
  -> __filterBy(IdentificacaoEntesPublicos): Contratos
  -> adiciona_dados_ipoc(Ipoc)
  -> adiciona_dados_tomadores(Tomadores)
  -> adiciona_dados_garantidores(Garantidores)
  -> tranform(): DadosCadip


DadosCadip()
  -> to_df()

OutPutRegistro1(DadosCadip)
  __format()
  -> to_df()
```






## Design de classes - 1
```
Contratos
Participantes
IdentificaoPessoas
DadosCadastrais
Tomadores
Garantidores
Ipocs

//contrato de entes publicos
IdentificacoesEntesPublicos(IdentificaoPessoas, DadosCadastrais)
ContratosEntesPublicos(Contratos, Participantes, IdentificacoesEntesPublicos)


//Tomador e Garantidor
DadosCadastraisEntesPublicos(DadosCadastrais, ContratosEntesPublicos)
  -getTomadores()
  -getGarantidores()


//Dados Cadip
DadosCadip(ContratosEntesPublicos)
  adicionaTomador()
  adicionaGarantidor()
  adicionaIpoc()

```


Exemplo de filter:
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Inicialização do Contexto do Glue e Spark
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --- 1. DEFINIÇÃO DOS PARÂMETROS DE FILTRO ---
# Define aqui os valores que queres filtrar
filtro_ano = "2026"
filtro_mes = "05"
filtro_dia = "25"
valor_coluna_comum = "CONCLUIDO"

# --- 2. LEITURA COM FILTRO DE PARTIÇÃO (Pushdown Predicate) ---
# O Glue vai ler APENAS a pasta S3 correspondente à data definida
dados_particionados = glueContext.create_dynamic_frame.from_catalog(
    database = "seu_banco_de_dados",              # Substitui pelo teu banco do Glue
    table_name = "sua_tabela",                     # Substitui pela tua tabela do Glue
    push_down_predicate = f"(ano == '{filtro_ano}' AND mes == '{filtro_mes}' AND dia == '{filtro_dia}')"
)

# --- 3. CONVERSÃO E FILTRO DA COLUNA COMUM ---
# Convertemos para DataFrame do Spark para facilitar a filtragem comum
df_spark = dados_particionados.toDF()

# Aplicamos o filtro na coluna comum (ex: status_pedido)
df_filtrado = df_spark.filter(df_spark["status_pedido"] == valor_coluna_comum)

# --- 4. EXIBIÇÃO DOS RESULTADOS (Para validação) ---
print(f"Quantidade de registos após os filtros: {df_filtrado.count()}")
df_filtrado.show(5)

job.commit()
```
