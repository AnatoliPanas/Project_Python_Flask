# from pydantic import BaseModel, EmailStr, validator, field_validator, Field, ValidationError, ValidationInfo
#
#
# class Address(BaseModel):
#     city: str
#     street: str
#     house_number: int
#
# class User(BaseModel):
#     name: str = Field(min_length=4,
#                       max_length=15,
#                       description="Name of user")
#     last_name: str = Field(default="Black",
#                            min_length=2,
#                            max_length=30)
#     age: int
#     email: EmailStr
#     address: Address
#     test: str
#     test1: str
#
#
#
#     @field_validator('age')
#     @classmethod
#     def validate_age(cls, value):
#         if value < 0 or value > 100:
#             raise ValueError("Возраст не верный")
#         return value
#
#
#     @field_validator('email')
#     @classmethod
#     def check_email_domain(cls, value: str) -> str:
#         allowed_domains = {"gmail.com",}
#         raw_email = value.split('@')[-1]
#         if raw_email not in allowed_domains:
#             raise ValueError(f"Email домен не из списка доступных: {allowed_domains}")
#         return value
#
#     @field_validator('test', 'test1')
#     @classmethod
#     def check_pusto(cls, value: str) -> str:
#         for item in value:
#             print(f'{item}+1')
#         if ' ' in value or not value.strip():
#             raise ValueError(f"Поля test, test1 не заполнены")
#         return value
#
# json_string = """
# {
#     "name": "Vlad",
#     "last_name": "K9",
#     "age": 28,
#     "email": "john.doe@gmail.com",
#     "address": {
#         "city": "New York",
#         "street": "St. Time Square",
#         "house_number": 2
#     },
#     "test": "yyy",
#     "test1": "ss"
# }
# """
#
# try:
#     user = User.model_validate_json(json_string)
#     print(user)
# except ValidationError as e:
#     print(e)

# =================================================================
# Field aliases
# =================================================================

# from pydantic import BaseModel, Field, AliasChoices
#
# class Item(BaseModel):
#     name: str
#     in_stock: bool = Field(validation_alias=AliasChoices("in_stock", "available", "In Stock"))
#
#
# # json_data = '{"name": "Laptop", "available": "true"}'
# json_data = ['{"name": "Laptop", "in_stock": "true"}',
#              '{"name": "Laptop", "available": "false"}',
#              '{"name": "Laptop", "In Stock": "false"}']
#
# for obj in json_data:
#     try:
#         item = Item.model_validate_json(obj)
#         print(item)
#     except ValueError as e:
#         print(e)

# =================================================================
# Field aliases
# =================================================================

from pydantic import BaseModel, Field, AliasChoices

class Event(BaseModel):
    title: str = Field(min_length=4)

    class Config:
        validate_assignment = True

        str_min_length = 4
        str_strip_whitespace = True


event = Event(title="     1234")
print(event)

# event.title = 123
# print(event)