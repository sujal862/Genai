from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin : str


class Patient(BaseModel):
    name:str
    gender: str
    age: int
    address: Address


address_dict = {'city': 'gurgao', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name' : 'nitish', 'gender' : 'male', 'age' : 35, 'address' : address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address.pin)



# ---------------------------------------------------
# model_dump converts the existing Pydantic model into a Python dictionary
# nested models are also converted into dictionaries
temp = patient1.model_dump()


# model_dump_json converts the model into a JSON string
temp1 = patient1.model_dump_json()


# include allows selecting specific fields only
# here only 'name' and 'gender' will appear in the output dictionary
temp2 = patient1.model_dump(include=['name', 'gender'])


print(temp)
print(type(temp))
