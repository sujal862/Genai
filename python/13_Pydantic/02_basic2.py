from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    # Annotated is used to attach metadata (Field validation + schema info)
    name: Annotated[
        str,
        Field(
            max_length=50,
            title='Name of the patient',   # title used in generated schema/docs (FastAPI / OpenAPI)
            description='Give the name of the patient in less than 50 chars',  # explanation shown in API docs
            examples=['Nitish', 'Amit']    # example values shown in documentation
        )
    ]

    age: int = Field(gt=0, lt=120)

    email: EmailStr
    linkedin_url: AnyUrl

    # strict=True disables automatic type conversion
    # Example: "75.2" (string) will NOT be converted to float and will raise ValidationError
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='is married?')]

    allergies: Optional[List[str]] = Field(max_length=5)

    contact_details: Dict[str, str]


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

patient1 = Patient(**patient_info)

insert_patient_data(patient1)