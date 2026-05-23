from pyspark.sql import DataFrame

from src.domain.contratos import Contratos
from src.domain.extract_contratos_fake import ExtractContratosFake
from src.domain.extract_participantes_fake import ExtractParticipantesFake
from src.domain.participantes import Participantes


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
    df_participantes.printSchema()
    df_participantes.show()


if __name__ == '__main__':
    run()


