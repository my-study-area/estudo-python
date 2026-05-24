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
DadosCadastrais
Tomadores
Garantidores
Ipocs
IdentificacaoEntesPublicos


EntesPublicos(Participantes, IdentificaoPessoas, DadosCadastrais)
  __data_frame
  __participantes
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


DadosCadip(DataFrame)
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

