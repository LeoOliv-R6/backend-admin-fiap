from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.endpoint_role import EndpointRole
from app.schemas.endpoint_role import EndpointRoleCreate, EndpointRoleUpdate, EndpointRoleMulti


class CRUDEndpointRole(CRUDBase[EndpointRole, EndpointRoleCreate, EndpointRoleUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[EndpointRole]:
        return db.query(EndpointRole).offset(skip).limit(limit).all()

    def get_multi_by_endpoint_id(self, db: Session, *, endpoint_id: int) -> List[EndpointRole]:
        return db.query(EndpointRole).filter(EndpointRole.endpoint_id == endpoint_id).all()

    def get_multi_by_role_id(self, db: Session, *, role_id: int) -> List[EndpointRole]:
        return db.query(EndpointRole).filter(EndpointRole.role_id == role_id).all()

    def get_by_endpoint_id_and_role_id(self, db: Session, *, endpoint_id: int, role_id: int) -> List[EndpointRole]:
        return db.query(EndpointRole).filter(EndpointRole.endpoint_id == endpoint_id, EndpointRole.role_id == role_id).first()

    def create_multi(self, db: Session, *, obj_in: EndpointRoleMulti) -> List[EndpointRole]:
        db_objs = list()
        for row in obj_in.endpoint_id:
            db_obj = EndpointRole(
                endpoint_id=row,
                role_id=obj_in.role_id
            )

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            db_objs.append(db_obj)

        return db_objs

    def remove_multi(self, db: Session, *, obj_out: EndpointRoleMulti) -> List[EndpointRole]:
        objs = list()
        for row in obj_out.endpoint_id:
            obj = self.get_by_endpoint_id_and_role_id(
                db,
                endpoint_id=row,
                role_id=obj_out.role_id
            )

            db.delete(obj)
            db.commit()
            objs.append(obj)

        return objs


endpoint_role = CRUDEndpointRole(EndpointRole)