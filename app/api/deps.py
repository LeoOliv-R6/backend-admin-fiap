from typing import Generator, List
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.ROOT_PATH}{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_allowed_endpoints(db: Session, role_id: int) -> List[str]:
    endpoint_roles = crud.endpoint_role.get_multi_by_role_id(db, role_id=role_id)

    endpoints = [endpoint_role.endpoint.url for endpoint_role in endpoint_roles]

    return endpoints


def get_current_administrator(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> models.Administrator:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM]
        )

        token_data = schemas.TokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    administrator = crud.administrator.get(db, id=token_data.sub)

    if not administrator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )

    current_endpoint = request.url.path.replace(settings.ROOT_PATH, "").upper()

    print(current_endpoint)
    allowed_endpoints = get_allowed_endpoints(db, administrator.role_id)

    if current_endpoint not in allowed_endpoints:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )

    return administrator