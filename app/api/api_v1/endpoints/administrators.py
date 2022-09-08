from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Administrator])
def read_administrators(
    db: Session = Depends(deps.get_db),
    administrator_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> List:
    if administrator_id:
        administrator = crud.administrator.get(db, id=administrator_id)

        return [administrator] if administrator else []

    else:
        administrators = crud.administrator.get_multi(db, skip=skip, limit=limit)

        return administrators


@router.post("/create", response_model=schemas.Administrator)
def create_administrator(
    *,
    db: Session = Depends(deps.get_db),
    administrator_in: schemas.AdministratorCreate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    administrator = crud.administrator.get_by_email(
        db,
        email=administrator_in.email
    )

    if administrator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An administrator with this email already exists in the system",
        )

    administrator = crud.administrator.create(db, obj_in=administrator_in)

    return administrator


@router.put("/update", response_model=schemas.Administrator)
def update_administrator(
    *,
    db: Session = Depends(deps.get_db),
    administrator_id: int,
    administrator_in: schemas.AdministratorUpdate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    administrator = crud.administrator.get(db, id=administrator_id)

    if not administrator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found",
        )

    administrator = crud.administrator.update(
        db,
        db_obj=administrator,
        obj_in=administrator_in
    )

    return administrator


@router.delete("/delete", response_model=schemas.Administrator)
def delete_administrator(
    *,
    db: Session = Depends(deps.get_db),
    administrator_id: int,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    administrator = crud.administrator.get(db, id=administrator_id)

    if not administrator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found",
        )

    administrator = crud.administrator.remove(db=db, id=administrator_id)

    return administrator