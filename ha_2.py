from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, model_validator, ValidationInfo
import re, json


# Модель Address
class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=2)
    house_number: int = Field(gt=0)

# Модель User
class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool = False
    address: Address

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise ValueError("Имя должно содержать только буквы")
        return value

    # @model_validator(mode='before')
    # @classmethod
    # def check_is_employed(cls, values):
    #     is_employed = values.get('is_employed')
    #     age = values.get('age')
    #     if is_employed and (age < 18 or age >= 65):
    #         raise ValueError("Возраст рабочего должен быть в диапазоне от 18 до 65 лет.")
    #     return values

    # @model_validator(mode='after')
    # def check_is_employed(self):
    #     is_employed = self.is_employed
    #     age = self.age
    #     if is_employed and (age < 18 or age >= 65):
    #         raise ValueError("Возраст рабочего должен быть в диапазоне от 18 до 65 лет.")
    #     return self

    @field_validator('is_employed')
    @classmethod
    def check_is_employed(cls, value: bool, values: ValidationInfo):
        age = values.data.get('age')
        if value and (age < 18 or age >= 65):
            raise ValueError("Возраст рабочего должен быть в диапазоне от 18 до 65 лет.")
        return value

def check_json(data_json):
    try:
        user = User.model_validate_json(data_json)
        print("Все значения прошли валидацию.")
        print("Серелизуем в JSON.")
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return f"Ошибка валидации: {e}"


# Пример ввода JSON
json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": false,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 23
    }
}"""

try:
    user = check_json(json_input)
    # user = User.model_validate_json(json_input)
    print(user)
except ValidationError as e:
    print(f"Ошибка валидации: {e}")