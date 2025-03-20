from pydantic import BaseModel

class Address(BaseModel):
    city: str
    street: str
    house: int

class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True
    address: list[Address] = []

address_data = {
    "city": "New York",
    "street": "st. Broadway",
    "house": 23
}

user_data = {
    "id": 1,
    "name": "Anatoli",
    "age": "39",
    "is_active": True,
    "address": [address_data]

}

user = User(**user_data)

print(user)


print("JSON" + '='*30 + "JSON")

class UserFromJSON(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True

user_json = """{
    "id": 1,
    "name": "Anatoli",
    "age": 39,
    "is_active": true
}"""

user_data = {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "is_active": True,
    "address": [
        {"city": "New York", "street": "5th Avenue", "house": 101},
        {"city": "Los Angeles", "street": "Sunset Blvd", "house": 202}
    ]
}

userfromjeson = UserFromJSON.model_validate_json(user_json)

print(user_json)
print(userfromjeson)
