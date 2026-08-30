from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, auth
from app.database import get_db

router = APIRouter(
    prefix="/patients",
    tags=["patient houses"]
)

@router.post("/", response_model=schemas.PatientHouseResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_house(
    patient_house: schemas.PatientHouseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Create a new patient house for the current user"""
    db_patient_house = models.PatientHouse(
        **patient_house.dict(),
        owner_id=current_user.id
    )
    
    db.add(db_patient_house)
    db.commit()
    db.refresh(db_patient_house)
    
    return db_patient_house

@router.get("/", response_model=schemas.PatientHouseList)
async def list_patient_houses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """List all patient houses for the current user"""
    patient_houses = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    total = db.query(models.PatientHouse)\
        .filter(models.PatientHouse.owner_id == current_user.id)\
        .count()
    
    return {
        "patient_houses": patient_houses,
        "total": total
    }

@router.get("/{patient_house_id}", response_model=schemas.PatientHouseResponse)
async def get_patient_house(
    patient_house_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get a specific patient house by ID"""
    patient_house = db.query(models.PatientHouse)\
        .filter(
            models.PatientHouse.id == patient_house_id,
            models.PatientHouse.owner_id == current_user.id
        )\
        .first()
    
    if not patient_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    return patient_house

@router.put("/{patient_house_id}", response_model=schemas.PatientHouseResponse)
async def update_patient_house(
    patient_house_id: int,
    patient_house_update: schemas.PatientHouseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Update a patient house"""
    db_patient_house = db.query(models.PatientHouse)\
        .filter(
            models.PatientHouse.id == patient_house_id,
            models.PatientHouse.owner_id == current_user.id
        )\
        .first()
    
    if not db_patient_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    # Update fields
    for key, value in patient_house_update.dict().items():
        setattr(db_patient_house, key, value)
    
    db.commit()
    db.refresh(db_patient_house)
    
    return db_patient_house

@router.delete("/{patient_house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_house(
    patient_house_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Delete a patient house"""
    db_patient_house = db.query(models.PatientHouse)\
        .filter(
            models.PatientHouse.id == patient_house_id,
            models.PatientHouse.owner_id == current_user.id
        )\
        .first()
    
    if not db_patient_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient house not found"
        )
    
    db.delete(db_patient_house)
    db.commit()
    
    return None