from __future__ import annotations
import re
from typing import Optional
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from src.domain.tomadores import Tomadores
from src.domain.garantidores import Garantidores
from src.domain.participantes import Participantes
from src.domain.identificacao_pessoas import IdentificacaoPessoas


class DadosCadastrais:
    __SETORES_EMPRESAS_PUBLICAS_DEFAULT = [1000, 2000]

    def __init__(self, data_frame: DataFrame, setores_empresas_publicas_customizado: Optional[str] = None) -> None:
        self.__data_frame = data_frame
        self.setores_empresas_publicas = setores_empresas_publicas_customizado

    @property
    def setores_empresas_publicas(self) -> list[int]:
        return self.__setores_empresas_publicas

    @setores_empresas_publicas.setter
    def setores_empresas_publicas(self, valor: Optional[str]) -> None:
        if valor is not None and self.__is_valid(valor):
            self.__setores_empresas_publicas = [int(x.strip()) for x in valor.split(',')]
        else:
            self.__setores_empresas_publicas = list(self.__SETORES_EMPRESAS_PUBLICAS_DEFAULT)

    @staticmethod
    def __is_valid(input_str: str) -> bool:
        return bool(re.fullmatch(r'\s*\d+\s*(,\s*\d+\s*)*', input_str))

    def is_empty(self) -> bool:
        return len(self.__data_frame.take(1)) == 0

    def get_tomadores(self, participantes: Participantes, identificacao_pessoas: IdentificacaoPessoas) -> Tomadores:
        df_participantes = participantes.to_df()
        df_identificacao = identificacao_pessoas.to_df()

        df_tomadores = (
            df_participantes
            .filter(col("tipo") == participantes.codigo_tipo_participante_tomador)
            .join(df_identificacao, "id_pessoa", "inner")
        )
        return Tomadores(df_tomadores)

    def get_garantidores(self, participantes: Participantes, identificacao_pessoas: IdentificacaoPessoas) -> Garantidores:
        df_participantes = participantes.to_df()
        df_identificacao = identificacao_pessoas.to_df()

        df_garantidores = (
            df_participantes
            .filter(col("tipo") == 3)
            .join(df_identificacao, "id_pessoa", "inner")
        )
        return Garantidores(df_garantidores)

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("identificacao_pessoa").cast("string").alias("id_pessoa"),
            col("setor_empresa").cast("string"),
            col("enderecos").alias("enderecos")
        )
