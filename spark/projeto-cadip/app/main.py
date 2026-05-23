from pyspark.sql import DataFrame

from src.domain.contratos import Contratos
from src.domain.extract_contratos_fake import ExtractContratosFake
from src.domain.extract_participantes_fake import ExtractParticipantesFake
from src.domain.participantes import Participantes
from src.domain.extract_identificacao_pessoas_fake import ExtractIdentificacaoPessoasFake
from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.domain.extract_dados_cadastrais_fake import ExtractDadosCadastraisFake
from src.domain.dados_cadastrais import DadosCadastrais


def print_hi():
    print(f'Hi')

def run():
    extract_contrato: ExtractContratosFake = ExtractContratosFake('db_custodia', 'tb_contratos')
    contratos: Contratos = extract_contrato.extract()
    df = contratos.to_df()
    # df.printSchema()
    # df.show(truncate=False)

    extract_participante: ExtractParticipantesFake = ExtractParticipantesFake('db_custodia', 'tb_participantes')
    participantes: Participantes = extract_participante.extract()
    df_participantes: DataFrame = participantes.to_df()
    # df_participantes.printSchema()
    # df_participantes.show()

    extract_ident_pessoas: ExtractIdentificacaoPessoasFake = ExtractIdentificacaoPessoasFake('db_custodia', 'tb_identificacao_pessoas')
    ident_pessoas: IdentificacaoPessoas = extract_ident_pessoas.extract()
    df_ident_pessoas: DataFrame = ident_pessoas.to_df()
    # df_ident_pessoas.printSchema()
    # df_ident_pessoas.show()

    extract_dados_cadastrais: ExtractDadosCadastraisFake = ExtractDadosCadastraisFake('db_custodia', 'tb_dados_cadastrais')
    dados_cadastrais: DadosCadastrais = extract_dados_cadastrais.extract()
    df_dados_cadastrais: DataFrame = dados_cadastrais.to_df()
    df_dados_cadastrais.printSchema()
    df_dados_cadastrais.show()


if __name__ == '__main__':
    run()


