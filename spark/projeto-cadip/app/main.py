import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark import SparkContext

from src.service.glue_configuration import GlueConfiguration
from src.etl.extract_builder import ExtractBuilderFactory

def run(glue_config: GlueConfiguration) -> None:
    print(f"Executando no ambiente: {glue_config.environment}")

    # 1. Cria o builder polimórfico
    builder = ExtractBuilderFactory.create(glue_config)


    # 3. Executa as extrações utilizando a abstração do builder
    print("\n--- Extraindo Contratos ---")
    contratos = builder.build_extract_contrato().extract()
    df_contratos = contratos.to_df()
    df_contratos.printSchema()
    df_contratos.show(truncate=False)

    print("\n--- Extraindo Participantes ---")
    participantes = builder.build_extract_participantes().extract()
    df_participantes = participantes.to_df()
    df_participantes.printSchema()
    df_participantes.show()

    print("\n--- Extraindo Identificação de Pessoas ---")
    ident_pessoas = builder.build_extract_identificao_pessoas().extract()
    df_ident_pessoas = ident_pessoas.to_df()
    df_ident_pessoas.printSchema()
    df_ident_pessoas.show()

    print("\n--- Extraindo Dados Cadastrais ---")
    dados_cadastrais = builder.build_extract_dados_cadastrais().extract()
    df_dados_cadastrais = dados_cadastrais.to_df()
    df_dados_cadastrais.printSchema()
    df_dados_cadastrais.show()

    print("\n--- Extraindo Posições Diárias ---")
    posicoes = builder.build_extract_posicoes_diarias().extract()
    df_posicoes = posicoes.to_df()
    df_posicoes.printSchema()
    df_posicoes.show()

    print("\n--- Extraindo IPOCs ---")
    ipocs = builder.build_extract_ipocs().extract()
    df_ipocs = ipocs.to_df()
    df_ipocs.printSchema()
    df_ipocs.show()


def run_job() -> None:
    """
    Exemplo básico de um Job no AWS Glue que lê dados do Lake Formation.
    Resolve internamente os parâmetros necessários do AWS Glue.
    """
    # 1. Resolve os argumentos do Glue internamente
    args_list = ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME']
    args = getResolvedOptions(sys.argv, args_list)
    
    database_name = args.get('DATABASE_NAME')
    table_name = args.get('TABLE_NAME')
    
    print(f"Iniciando a execução do Job: {args.get('JOB_NAME')}")
    print(f"Iniciando leitura da tabela catalogada: {database_name}.{table_name}")
    
    # 2. Inicializa o Spark Context e Glue Context reais do AWS Glue
    sc = SparkContext.getOrCreate()
    glue_context = GlueContext(sc)
    
    # 3. Lê a tabela do Lake Formation através do catálogo (Dynamic Frame)
    dynamic_frame: DynamicFrame = glue_context.create_dynamic_frame.from_catalog(
        database=database_name,
        table_name=table_name
    )
    
    # 4. Ações básicas: log de contagem e esquema para validação
    print(f"Total de registros lidos: {dynamic_frame.count()}")
    dynamic_frame.printSchema()


if __name__ == '__main__':
    # 1. Resolve os argumentos do Glue utilizando a lista definida
    args_list = ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME', 'ENVIRONMENT']
    args = getResolvedOptions(sys.argv, args_list)
    
    # 2. Inicializa o Spark e Glue Context nativos
    sc = SparkContext.getOrCreate()
    glue_context = GlueContext(sc)

    # 3. Instancia a configuração desacoplada e chama run
    glue_config = GlueConfiguration(args, glue_context)
    run_job()




