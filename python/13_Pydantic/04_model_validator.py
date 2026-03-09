from pydantic import BaseModel, EmailStr, AnyUrl, model_validator
from typing import List, Dict, Optional

# validate(2 field) : if a patient age > 60 then in his contact_details there should be emergency phone number
class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    weight: float
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

    # model_validator runs validation on the whole model instead of a single field
    # mode='after' means it runs AFTER all fields are validated and the model object is created
    @model_validator(mode='after')
    def validate_emergency_contacts(cls, model):
        # model contains the fully created Patient object (object instance)
        # so we can access all fields like model.age, model.contact_details
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have emergency contacts')
        return model

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')


patient_info = {
    'name': 'nitish',
    'age': 44,
    'email': 'abc@hdfc.com',
    'linkedin_url': 'http://linkedin.com/333',
    'weight': 75.2,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'abc@gmail.com',
        'phone': '2353462'
    }
}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)