from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Patient House schemas
class PatientHouseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    phone_number: Optional[str] = None

class PatientHouseCreate(PatientHouseBase):
    pass

class PatientHouseResponse(PatientHouseBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PatientHouseList(BaseModel):
    patient_houses: List[PatientHouseResponse]
    total: int