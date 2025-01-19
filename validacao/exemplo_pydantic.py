# from pydantic import BaseModel, EmailStr, ValidationError, Field
# from typing import List
#
# class Endereco(BaseModel):
#     rua: str
#     numero: int = Field(ge=0, description="Número deve ser maior ou igual a 0")
#
# class User(BaseModel):
#     nome: str
#     email: EmailStr
#     idade: int = Field(gt=0, description="Idade deve ser maior que 0")
#     enderecos: List[Endereco]
#
# # Dados a serem validados
# data = {
#     "nome": "João da Silva",
#     # "email": "joao@example.com",
#     "email": "joao@examplecom",
#     # "idade": 30,
#     "idade": 0,
#     "enderecos": [
#         {"rua": "Rua dos Bobos", "numero": 0}
#     ]
# }
#
# try:
#     user = User(**data)
#     print(user)
# except ValidationError as e:
#     print(e.json())



# from pydantic import (
#     BaseModel,
#     ValidationError,
#     ValidationInfo,
#     field_validator,
# )
#
#
# class UserModel(BaseModel):
#     name: str
#     id: int
#
#     @field_validator('name')
#     @classmethod
#     def name_must_contain_space(cls, v: str) -> str:
#         if ' ' not in v:
#             raise ValueError('must contain a space')
#         return v.title()
#
#     # you can select multiple fields, or use '*' to select all fields
#     @field_validator('id', 'name')
#     @classmethod
#     def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
#         if isinstance(v, str):
#             # info.field_name is the name of the field being validated
#             is_alphanumeric = v.replace(' ', '').isalnum()
#             assert is_alphanumeric, f'{info.field_name} must be alphanumeric'
#         return v
#
#
# # print(UserModel(name='John Doe', id=1))
#
#
# try:
#     UserModel(name=12, id=1)
#
# except ValidationError as e:
#     print(e.json())




# from pydantic import BaseModel, field_validator
# from typing import Optional
#
#
# class User(BaseModel):
#     name: str
#     age: int
#     email: Optional[str] = None
#
#     @field_validator('name')
#     def name_must_contain_space(cls, value):
#         if ' ' not in value:
#             raise ValueError('Nome deve conter espaço')
#         return value
#
#     @field_validator('name')
#     def name_is_required(cls, value):
#         if value is None:
#             raise ValueError('Nome obrigatório')
#         return value
#
#
# try:
#     user = User(name='John Doe', age=30)
#     # print(user)
#
#     # invalid_user = User(name='JohnDoe', age=30)
#     invalid_user = User(age=30)
# except ValueError as e:
#     print(str(e))


from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator

class User(BaseModel):
    nome: str = Field(..., description="O nome do usuário.")
    email: EmailStr = Field(..., description="Um endereço de email válido.")
    idade: int = Field(..., gt=0, description="A idade deve ser maior que 0.")

    # Customizando validação do email
    @field_validator("email")
    def validar_email(cls, value):
        if "@" not in value:
            raise ValueError("Por favor, forneça um email válido contendo '@'.")
        return value

    # Customizando validação da idade
    @field_validator("idade", mode="before")
    def validar_idade(cls, value):
        if value <= 0:
            raise ValueError("A idade deve ser maior que zero.")
        return value

# Testando com dados inválidos
dados = {
    "nome": "João",
    "email": "emailinvalido",
    "idade": -5
}


def traduzir_erros(validation_error: ValidationError) -> list[dict]:
    erros = []
    for err in validation_error.errors():
        if err["loc"] == ("email",):
            err["msg"] = "O campo 'email' deve conter um '@'."
        elif err["loc"] == ("idade",):
            err["msg"] = "A idade deve ser maior que zero."
        erros.append(err)
    return erros

try:
    usuario = User(**dados)
except ValidationError as e:
    erros_personalizados = traduzir_erros(e)
    print(erros_personalizados)
