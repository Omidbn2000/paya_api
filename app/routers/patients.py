# app/routers/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patient Houses"])

@router.get("/", response_model=schemas.PatientHouseList)
async def get_patient_houses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all patient houses for the current user"""
    houses = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    total = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .count()
    
    return {
        "patient_houses": houses,
        "total": total
    }

@router.post("/", response_model=schemas.PatientHouseResponse)
async def create_patient_house(
    house: schemas.PatientHouseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new patient house"""
    db_house = models.PatientHouse(
        name=house.name,
        latitude=house.latitude,
        longitude=house.longitude,
        address=house.address,
        phone_number=house.phone_number,
        owner_id=current_user.id
    )
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

@router.get("/{house_id}", response_model=schemas.PatientHouseResponse)
async def get_patient_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific patient house"""
    house = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.id == house_id)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .first()
    
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    return house

@router.put("/{house_id}", response_model=schemas.PatientHouseResponse)
async def update_patient_house(
    house_id: int,
    house_update: schemas.PatientHouseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a patient house"""
    house = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.id == house_id)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .first()
    
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    house.name = house_update.name
    house.latitude = house_update.latitude
    house.longitude = house_update.longitude
    house.address = house_update.address
    house.phone_number = house_update.phone_number
    
    db.commit()
    db.refresh(house)
    return house

@router.delete("/{house_id}")
async def delete_patient_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a patient house"""
    house = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.id == house_id)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .first()
    
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    db.delete(house)
    db.commit()
    
    return {"message": "Patient house deleted successfully"}