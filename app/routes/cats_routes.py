from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import SpyCat
import requests
from app.schemas.cats_schemas import SpyCatCreate, SpyCatResponse, SpyCatUpdate

router = APIRouter(prefix="/spy_cats")


CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


def is_valid_breed(breed: str) -> None:
    """The function checks if the specified breed exists"""
    response = requests.get(CAT_API_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error fetching breeds")

    breeds = response.json()
    valid_breeds = [b['name'].lower() for b in breeds]

    if breed.lower() not in valid_breeds:
        raise HTTPException(status_code=400, detail="Invalid breed")


# Spy Cat Routes
@router.post("/create/", response_model=SpyCatResponse, status_code=201)
async def create_spy_cat(cat: SpyCatCreate, db: Session = Depends(get_db)):
    # Validate breed with TheCatAPI before adding to the database
    is_valid_breed(cat.breed)

    db_cat = SpyCat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete("/{spy_cat_id}")
def delete_spy_cat(spy_cat_id: int, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    db.delete(db_spy_cat)
    db.commit()
    return {"message": "Spy cat deleted"}


@router.put("/{spy_cat_id}", response_model=SpyCatResponse)
def update_spy_cat(spy_cat_id: int, spy_cat: SpyCatUpdate, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    db_spy_cat.salary = spy_cat.salary
    db.commit()
    db.refresh(db_spy_cat)
    return db_spy_cat


@router.get("/list", response_model=List[SpyCatResponse])
def list_spy_cats(db: Session = Depends(get_db)):
    return db.query(SpyCat).all()


@router.get("/{spy_cat_id}", response_model=SpyCatResponse)
def get_spy_cat(spy_cat_id: int, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    return db_spy_cat
