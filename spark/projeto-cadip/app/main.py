from pyspark.sql import DataFrame

from src.domain.contratos import Contratos
from src.domain.extract_contratos_fake import ExtractContratosFake


def print_hi():
    print(f'Hi')

def run():
    extract_contrato: ExtractContratosFake = ExtractContratosFake('db_custodia', 'tb_contratos')
    contratos: Contratos = extract_contrato.extract()
    df = contratos.to_df()
    df.printSchema()
    df.show(truncate=False)

if __name__ == '__main__':
    run()


