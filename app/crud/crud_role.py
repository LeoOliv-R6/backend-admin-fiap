from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name_and_level(self, db: Session, *, name: str, level: int) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name, Role.level == level).first()

    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        db_obj = Role(
            name=obj_in.name.upper(),
            level=obj_in.level,
            description=obj_in.description.upper()
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: Role, obj_in: Union[RoleUpdate, Dict[str, Any]]) -> Role:
        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "name" in update_data:
            uppercase_name = str(update_data["name"]).upper()

            update_data["name"] = uppercase_name

        if "description" in update_data:
            uppercase_description = str(update_data["description"]).upper()

            update_data["description"] = uppercase_description

        return super().update(db, db_obj=db_obj, obj_in=update_data)


role = CRUDRole(Role)