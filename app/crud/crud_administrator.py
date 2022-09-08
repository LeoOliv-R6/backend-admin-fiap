from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.administrator import Administrator
from app.schemas.administrator import AdministratorCreate, AdministratorUpdate
from app.core.security import get_password_hash, verify_password


class CRUDAdministrator(CRUDBase[Administrator, AdministratorCreate, AdministratorUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Administrator]:
        return db.query(Administrator).filter(Administrator.email == email.lower()).first()

    def create(self, db: Session, *, obj_in: AdministratorCreate) -> Administrator:
        db_obj = Administrator(
            name=obj_in.name,
            email=obj_in.email.lower(),
            hashed_password=get_password_hash(obj_in.password),
            document=obj_in.document,
            role_id=obj_in.role_id
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: Administrator, obj_in: Union[AdministratorUpdate, Dict[str, Any]]) -> Administrator:
        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "email" in update_data:
            lowercase_email = str(update_data["email"]).lower()

            update_data["email"] = lowercase_email

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])

            del update_data["password"]

            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Administrator]:
        administrator = self.get_by_email(db, email=email)

        if not administrator:
            return None

        if not verify_password(password, administrator.hashed_password):
            return None

        return administrator

    def is_active(self, administrator: Administrator) -> bool:
        return administrator.is_active


administrator = CRUDAdministrator(Administrator)