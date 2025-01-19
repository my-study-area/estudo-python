from cerberus import Validator

# Definindo o esquema de validação
schema = {
    'nome': {'type': 'string'},
    'email': {'type': 'string', 'regex': r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    'idade': {'type': 'integer', 'min': 0},
    'enderecos': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'rua': {'type': 'string'},
                'numero': {'type': 'integer', 'min': 0}
            }
        }
    }
}

# schema = {
#     'nome': {'type': 'string', 'error_messages': {'required': 'O campo "nome" é obrigatório.'}},
#     'idade': {'type': 'integer', 'min': 18, 'error_messages': {'min': 'Você deve ter pelo menos 18 anos.'}}
# }

# Dados a serem validados
document = {
    "nome": "João da Silva",
    # "email": "joao@example.com",
    "email": "joaoexamplecom",
    "idade": -30,
    "enderecos": [
        {
            "rua": "Rua dos Bobos",
            "numero": 0
        }
    ]
}

# Criando um validador e validando os dados
v = Validator(schema)
if v.validate(document):
    print("Dados válidos!")
else:
    print(v.errors)
