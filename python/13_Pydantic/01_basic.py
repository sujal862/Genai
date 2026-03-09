from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

#Schema
class Patient(BaseModel):
    name: str = Field(max_length=50) 
    age: int = Field(gt=0, lt=120) ## data validation
    email : EmailStr  # validates that value is a proper email format
    linkedin_url: AnyUrl  # validates that the value is a valid URL
    weight: float = Field(gt=0) # its value cant be less then 0
    married: bool = False # default value. If user doesn't provide it, False will be used
    allergies: Optional[List[str]] = Field(max_length=5)   #  Optional means the field can be provided OR skipped /  #allergies is list of strings
    contact_details: Dict[str, str]

# code is creating a data model for a patient and validating the data before using it.
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
    'email': 'abc@gmail.com',
    'linkedin_url': 'http://linkedin.com/333',
    'weight': 75.2,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'abc@gmail.com',
        'phone': '2353462'
    }
}
patient1 = Patient(**patient_info) # dictionary unpacking : python converts it into : Patient(name='nitish', age=30)

# Now patient1 is a validated Patient object
# If any field had wrong type (invalid email, wrong url, etc)
# Pydantic would raise a ValidationError before this step
insert_patient_data(patient1)