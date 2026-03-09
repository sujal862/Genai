from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

    @computed_field  
    # tells Pydantic that this is a computed field (not provided by user input)
    # it will be automatically included when model is serialized (model_dump / API response)

    @property  
    # makes this behave like an attribute instead of a method
    # so we can access it as patient.bmi instead of patient.bmi()

    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        # round(..., 2) keeps only 2 decimal places
        return bmi
    
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('BMI', patient.bmi)
    print('inserted')


patient_info = {
    'name': 'nitish',
    'age': 44,
    'email': 'abc@hdfc.com',
    'weight': 75.2,
    'height': 113,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'abc@gmail.com',
        'phone': '2353462'
    }
}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)