from pydantic import BaseModel, EmailStr, AnyUrl, field_validator
from typing import List, Dict, Optional, Annotated

# checking if patient is from hdfc or icici bank by checking email
class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    weight: float
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

    # # tells Pydantic to run this function whenever the 'email' field is validated
    @field_validator('email') 
    @classmethod # method receives the class (cls) instead of an object instance (self)
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1] #[-1] means last element of the list.
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domains')

        return value

    # converts name to upper case
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
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
    'age': 30,
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