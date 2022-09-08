from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.EndpointRole])
def read_endpoint_roles(
    db: Session = Depends(deps.get_db),
    endpoint_id: int = None,
    role_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> List:
    if endpoint_id and role_id:
        endpoint_role = crud.endpoint_role.get_by_endpoint_id_and_role_id(
            db,
            endpoint_id=endpoint_id,
            role_id=role_id
        )

        return [endpoint_role] if endpoint_role else []

    elif endpoint_id:
        endpoint_roles = crud.endpoint_role.get_multi_by_endpoint_id(
            db,
            endpoint_id=endpoint_id
        )

    elif role_id:
        endpoint_roles = crud.endpoint_role.get_multi_by_role_id(
            db,
            role_id=role_id
        )

    else:
        endpoint_roles = crud.endpoint_role.get_multi(
            db,
            skip=skip,
            limit=limit
        )

    return endpoint_roles


@router.post("/create", response_model=List[schemas.EndpointRole])
def create_endpoint_role(
    *,
    db: Session = Depends(deps.get_db),
    endpoint_role_in: schemas.EndpointRoleMulti,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    for row in endpoint_role_in.endpoint_id:
        endpoint_role = crud.endpoint_role.get_by_endpoint_id_and_role_id(
            db,
            endpoint_id=row,
            role_id=endpoint_role_in.role_id
        )

        if endpoint_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An association between endpoint and role already exists in the system",
            )

        endpoint = crud.endpoint.get(db, id=row)
        role = crud.role.get(db, id=endpoint_role_in.role_id)

        if not endpoint or not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endpoints or role not found",
            )

    endpoint_roles = crud.endpoint_role.create_multi(db, obj_in=endpoint_role_in)

    return endpoint_roles


@router.delete("/delete", response_model=List[schemas.EndpointRole])
def delete_endpoint_role(
    *,
    db: Session = Depends(deps.get_db),
    endpoint_role_out: schemas.EndpointRoleMulti,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    for row in endpoint_role_out.endpoint_id:
        endpoint_role = crud.endpoint_role.get_by_endpoint_id_and_role_id(
            db,
            endpoint_id=row,
            role_id=endpoint_role_out.role_id
        )

        if not endpoint_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endpoint role not found"
            )

    endpoint_roles = crud.endpoint_role.remove_multi(
        db,
        obj_out=endpoint_role_out
    )

    return endpoint_roles