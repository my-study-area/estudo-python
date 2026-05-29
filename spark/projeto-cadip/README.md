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
PosicoesDiaria
DadosCadastrais
IdentificaoPessoas
Participantes
Ipocs


Tomadores
Garantidores
EntesPublicosPriorizado
  __numero_contrato
  __id_pessoa
  __tipo_participante
  __municipio
  __uf
  to_df()


EntesPublicos(DadosCadastrais, IdentificaoPessoas, Participantes)
  __dados_cadastrais
  __identificao_pessoas
  __participantes
  __entes_publicos_priorizados
  __data_frame
  -> _join()
  -> _filter()
  -> identificador
  -> tomadores
  -> garantidores
  -> to_df()


DadosCadip(Contratos, PosicoesDiaria)
  -> adiciona_dados_ipoc(Ipoc)
  -> adiciona_entes_publicos(EntesPublicos)
  ->__filter_by(EntesPublicos)
  -> to_df()


Transformer(DadosCadip, EntesPublicos, Ipocs)
  __dados_cadip
  __entes_publicos
  __data_frame
  __ipocs
  -> tranform(): DadosCadip




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


## Exemplo modularização
No Python, o conceito é exatamente o mesmo: queremos esconder a complexidade interna e expor apenas o que é necessário. Porém, a forma de fazer isso é filosoficamente diferente do Java.

Enquanto o Java usa modificadores rígidos de visibilidade (`public`, `private`, `protected`) e o sistema de módulos (`module-info.java`), o Python adota a filosofia de que **"somos todos adultos consentidos aqui"** (*we are all consenting adults here*). Isso significa que o Python foca em **convenções e barreiras lógicas**, em vez de restrições rígidas do compilador.

Aqui está como replicamos o encapsulamento e a modularização do Java no Python:

---

### 1. Visibilidade de Métodos e Atributos (O "Private" do Python)

O Python não impede fisicamente ninguém de acessar um atributo, mas usa prefixos de *underscores* (`_`) para sinalizar a visibilidade.

#### O "Protected" (Convenção de um underscore `_`)

Se você quer que um método ou atributo seja tratado como interno (privado daquele módulo/classe), você começa o nome dele com **um único underscore**.

```python
class ProcessadorPagamento:
    def __init__(self):
        self._api_key = "segredo_123"  # Convenção: por favor, não mexa aqui fora da classe

    def _conectar_ao_banco(self):
        # Método interno/auxiliar
        print("Conectando...")

    def processar(self):
        # Único método que o mundo exterior deveria chamar
        self._conectar_ao_banco()
        print("Pago!")

```

#### O "Private" Forte (Dois underscores `__`)

Se você usar **dois underscores**, o Python ativa o *Name Mangling* (desfiguração de nomes). Ele transforma internamente o nome da variável para incluir o nome da classe, dificultando o acesso acidental (embora ainda não seja 100% impossível).

```python
class ContaBancaria:
    def __init__(self):
        self.__saldo = 0  # O Python muda o nome disso para _ContaBancaria__saldo

```

---

### 2. Estrutura de Módulos e Pacotes

No Java, você usa pacotes para organizar arquivos. No Python:

* **Módulo:** É simplesmente qualquer arquivo `.py`.
* **Pacote:** É uma pasta que contém arquivos `.py`.

#### Controlando o que é exportado com `__all__`

Para ocultar a complexidade de um pacote inteiro e mostrar apenas "o necessário" para os outros módulos (como o sistema de módulos do Java), usamos o arquivo especial `__init__.py` dentro da pasta do pacote e a lista `__all__`.

Imagine a seguinte estrutura de pastas:

```text
meu_projeto/
│
├── meu_pacote/
│   ├── __init__.py
│   ├── calculos_complexos.py
│   └── utilitarios_internos.py
│
└── principal.py

```

Dentro de `meu_pacote/calculos_complexos.py`, você tem várias funções, mas só quer expor a função `calcular_tudo`.

No seu `meu_pacote/__init__.py`, você define o que fica visível publicamente quando alguém importa seu pacote:

```python
# meu_pacote/__init__.py

# Importamos internamente o que precisamos
from .calculos_complexos import calcular_tudo, _funcao_ajuda_interna

# Definimos estritamente o que o "mundo exterior" pode ver
__all__ = ['calcular_tudo']

```

Pronto! Se alguém no arquivo `principal.py` tentar fazer isso:

```python
from meu_pacote import *
# Apenas 'calcular_tudo' será importado. '_funcao_ajuda_interna' foi ocultada.

```

---

### Resumo Comparativo: Java vs Python

| Conceito | Como é no Java | Como é no Python |
| --- | --- | --- |
| **Esconder membro da classe** | Modificador `private` | Prefixo `_` (convenção) ou `__` (mangling) |
| **Membro visível apenas no pacote** | Visibilidade *package-private* (padrão) | Prefixo `_` em funções ou classes do módulo |
| **Expor a API pública do pacote** | `module-info.java` (exports...) | Lista `__all__` dentro do arquivo `__init__.py` |

Em suma: no Python, você alcança a modularização organizando seu código em arquivos e pastas, usando o `__init__.py` como a "fachada" (Facade) do seu módulo, e confiando nos underscores para avisar outros desenvolvedores sobre o que é público e o que é privado.
