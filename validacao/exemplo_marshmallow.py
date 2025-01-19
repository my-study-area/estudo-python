from os import error

from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, error="Pelo menos um"), error_messages={"required": "Campo obrigatório"})
    age = fields.Int(validate=validate.Range(min=18, error="Tem que ser maior que 18"))
    email = fields.Str(
        required=True, validate=validate.Email(error="Email não é valido")
    )


# Create an instance of the UserSchema
user_schema = UserSchema()

# Define some data to validate
data = {
    'name': 'John Doe',
    'age': 25,
    'email': 'john@example.com'
}

# Validate the data against the schema
result = user_schema.load(data)

# Print the validated data
print(result)
# Output: {'name': 'John Doe', 'age': 25, 'email': 'john@example.com'}

# Define some invalid data
invalid_data = {
    # 'name': 'Jane Smith',
    'name': 'J',
    'age': 17,
    'email': 'invalid-email'
}

# Attempt to validate the invalid data
try:
    user_schema.load(invalid_data)
except ValidationError as e:
    print(str(e))