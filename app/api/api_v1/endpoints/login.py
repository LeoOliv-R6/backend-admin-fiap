from datetime import timedelta
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict:
    administrator = crud.administrator.authenticate(
        db=db,
        email=form_data.username.lower(),
        password=form_data.password
    )

    if not administrator:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    elif not crud.administrator.is_active(administrator):
        raise HTTPException(status_code=400, detail="Inactive admin")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(
            administrator.id,
            expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


@router.post("/test-token", response_model=schemas.Administrator)
def test_token(
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> Dict:
    return current_administrator


@router.get("/permissions", response_model=List[schemas.Endpoint])
def read_permissions(
    db: Session = Depends(deps.get_db),
    current_administrator: models.Administrator = Depends(
        deps.get_current_administrator
    )
) -> List:
    endpoint_roles = crud.endpoint_role.get_multi_by_role_id(
        db,
        role_id=current_administrator.role_id
    )

    endpoints = [endpoint_role.endpoint for endpoint_role in endpoint_roles]

    return endpoints