from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    role_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> List:
    if role_id:
        role = crud.role.get(db, id=role_id)

        return [role] if role else []

    else:
        roles = crud.role.get_multi(db, skip=skip, limit=limit)

        return roles


@router.post("/create", response_model=schemas.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    role = crud.role.get_by_name_and_level(
        db,
        name=role_in.name,
        level=role_in.level
    )

    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A role with this name and level already exists in the system",
        )

    role = crud.role.create(db, obj_in=role_in)

    return role


@router.put("/update", response_model=schemas.Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: schemas.RoleUpdate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    role = crud.role.get(db, id=role_id)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    role = crud.role.update(
        db,
        db_obj=role,
        obj_in=role_in
    )

    return role


@router.delete("/delete", response_model=schemas.Role)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    role = crud.role.get(db, id=role_id)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    role = crud.role.remove(db=db, id=role_id)

    return role