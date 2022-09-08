from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Endpoint])
def read_endpoints(
    db: Session = Depends(deps.get_db),
    endpoint_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> List:
    if endpoint_id:
        endpoint = crud.endpoint.get(db, id=endpoint_id)

        return [endpoint] if endpoint else []

    else:
        endpoints = crud.endpoint.get_multi(db, skip=skip, limit=limit)

        return endpoints


@router.post("/create", response_model=schemas.Endpoint)
def create_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    endpoint_in: schemas.EndpointCreate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    endpoint = crud.endpoint.get_by_url(db, url=endpoint_in.url)

    if endpoint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An endpoint with this url already exists on the system",
        )

    endpoint = crud.endpoint.create(db, obj_in=endpoint_in)

    return endpoint


@router.put("/update", response_model=schemas.Endpoint)
def update_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    endpoint_id: int,
    endpoint_in: schemas.EndpointUpdate,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    endpoint = crud.endpoint.get(db, id=endpoint_id)

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    endpoint = crud.endpoint.update(
        db,
        db_obj=endpoint,
        obj_in=endpoint_in
    )

    return endpoint


@router.delete("/delete", response_model=schemas.Endpoint)
def delete_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    endpoint_id: int,
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    endpoint = crud.endpoint.get(db, id=endpoint_id)

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    endpoint = crud.endpoint.remove(db=db, id=endpoint_id)

    return endpoint