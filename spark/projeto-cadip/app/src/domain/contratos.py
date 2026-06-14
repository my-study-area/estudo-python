from __future__ import annotations

import logging

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_sub, current_date

logger = logging.getLogger(__name__)

class Contratos:
    def __init__(self, data_frame: DataFrame) -> None:
        self.__data_frame = data_frame

    def is_empty(self) -> bool:
        return len(self.__data_frame.take(1)) == 0

    def filter_by_entes_publicos(
        self,
        participantes,
        identificao_pessoas,
        dados_cadastrais,
    ) -> Contratos:
        df_participantes = participantes.to_df()
        df_identificacao = identificao_pessoas.to_df()
        df_dados_cadastrais = dados_cadastrais.to_df()

        cond_participantes = col("participantes.numero_contrato") == col("contratos.numero_contrato_servico").cast("string")
        cond_identificacao = col("identificacao.id_pessoa") == col("participantes.id_pessoa")
        cond_dados_cadastrais = col("dados.id_pessoa") == col("identificacao.id_pessoa")

        df_filtrado = (
            self.__data_frame.alias("contratos")
            .join(df_participantes.alias("participantes"), cond_participantes, "inner")
            .join(df_identificacao.alias("identificacao"), cond_identificacao, "inner")
            .join(df_dados_cadastrais.alias("dados"), cond_dados_cadastrais, "inner")
            .filter(col("participantes.tipo") == participantes.codigo_tipo_participante_tomador)
            .filter(col("contratos.data_contratacao") == date_sub(current_date(), 1))
            .filter(col("dados.setor_empresa").cast("int").isin(dados_cadastrais.setores_empresas_publicas))
            .select("contratos.*")
        )
        logger.info('Total de registros filtrados: %s', df_filtrado.count())
        return Contratos(df_filtrado)

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("numero_contrato_servico").cast("string").alias("numero_contrato"),
            col("valor_contratacao").cast("string").alias("valor"),
            col("data_contratacao").cast("date").alias("data"),
        )
