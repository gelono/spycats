from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Mission, Target, SpyCat
from app.schemas.missions_schemas import MissionCreate, MissionResponse, MissionUpdate
from app.schemas.targets_schemas import TargetResponse, TargetUpdate

router = APIRouter(prefix="/missions")


@router.post("/create/", response_model=MissionResponse, status_code=201)
def create_mission(mission_data: MissionCreate, db: Session = Depends(get_db)):
    # Checking if a cat exists in the database
    cat = db.query(SpyCat).filter(SpyCat.id == mission_data.cat_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail="Spy Cat not found")

    # Create targets
    targets = [
        Target(
            name=target['name'],
            country=target['country'],
            notes=target['notes'],
            is_complete=target.get('is_complete', False)
        )
        for target in mission_data.targets
    ]

    # Create a mission object
    mission = Mission(
        cat_id=mission_data.cat_id,
        is_complete=mission_data.is_complete,
        targets=targets
    )

    # Adding mission and targets to the db
    db.add(mission)
    db.commit()
    db.refresh(mission)

    return mission


@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    # If the mission is already assigned to the cat, then deletion is impossible
    if db_mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission is assigned to a cat and cannot be deleted")

    db.delete(db_mission)
    db.commit()
    return {"message": "Mission deleted"}


@router.put("/{mission_id}", response_model=MissionResponse)
def update_mission(mission_id: int, mission_data: MissionUpdate, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Checking if the mission is complete
    if db_mission.is_complete:
        raise HTTPException(status_code=400, detail="Mission is already complete")

    db_mission.is_complete = mission_data.is_complete
    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.put("/target/{target_id}", response_model=TargetResponse)
def update_target(target_id: int, target_data: TargetUpdate, db: Session = Depends(get_db)):
    # We get the target from the database
    db_target = db.query(Target).filter(Target.id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")

    # We receive a mission to which the goal is attached
    db_mission = db.query(Mission).filter(Mission.id == db_target.mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission associated with this target not found")

    # Checking if the mission is complete
    if db_mission.is_complete:
        raise HTTPException(status_code=400, detail="Mission is already complete. Target cannot be updated")

    # Checking if the target is completed
    if db_target.is_complete:
        raise HTTPException(status_code=400, detail="Cannot update target after completion")

    # Updating target data
    db_target.notes = target_data.notes if target_data.notes else db_target.notes
    db_target.is_complete = target_data.is_complete
    db.commit()
    db.refresh(db_target)

    return db_target


@router.put("/{mission_id}/assign_cat/{cat_id}", response_model=MissionResponse)
def assign_cat_to_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    # Checking the existence of the mission
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Checking the existence of a cat
    db_cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    # Check if the mission is complete, as completed missions cannot be updated.
    if db_mission.is_complete:
        raise HTTPException(status_code=400, detail="Mission is already completed and cannot be assigned a cat")

    # Assigning a cat to a mission
    db_mission.cat_id = cat_id
    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.get("/list", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    # Checking if a record exists in the database
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return db_mission
