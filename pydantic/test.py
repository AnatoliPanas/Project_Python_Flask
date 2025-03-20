from pydantic import BaseModel, field_validator, Field, ValidationInfo



class User(BaseModel):
    age: int
    last_name: str
    name: str = Field(min_length=4)
    is_adult: bool = False

    # @field_validator('is_adult')
    # def validate_is_adult(cls, value, values: ValidationInfo):
    #     age = values.data.get('age')
    #     if age is not None and age >= 18:
    #         return True
    #     return True

    # @field_validator('is_employed')
    # @classmethod
    # def check_is_employed(cls, value: bool, values: ValidationInfo):
    #     age = values.data.get('age')
    #     is_adult = value

    # @field_validator("name", "last_name", mode='before')
    # @classmethod
    # def validator_empty(cls, value):
    #     if value == '' or not value.strip():
    #         raise ValueError("Пусто")
    #     return value

    @field_validator("name", mode='before')
    @classmethod
    def validator_empty(cls, value, values: ValidationInfo):
        age_temp = values.data.get("age")
        las_name_temp = values.data.get("last_name")
        if age_temp <= 0:
            raise ValueError("Ошибка < 0")
        if len(las_name_temp) < 4:
            raise ValueError("Ошибка < 4")
        if value == '' or not value.strip():
            raise ValueError("Пусто")
        return value


user = User(name="Anatoli", last_name="Panas", age=20)
print(user)  # name='Anatoli' age=20 is_adult=True