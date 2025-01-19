import jsonschema
import json

data = {
    # "nome": "João da Silva",
    "nome": "",
    # "email": "joao@example.com",
    "email": "joaoexample.com",
    "idade": 30,
    # "idade": "30",
    "enderecos": [
        {
            "rua": "Rua dos Bobos",
            "numero": 0
        }
    ]
}

schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string", "minLength": 1,"error_msg": "faltou o nome"},
        "email": {"type": "string", "format": "email"},
        "idade": {"type": "integer"},
        "enderecos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "rua": {"type": "string"},
                    "numero": {"type": "integer"}
                },
                "required": ["rua", "numero"]
            }
        }
    },
    "required": ["nome", "email", "idade", "enderecos"]
}

try:
    jsonschema.validate(data, schema)
    print("JSON válido de acordo com o esquema")
except jsonschema.exceptions.ValidationError as e:
    print("JSON inválido:", e)