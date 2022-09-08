from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.endpoint import Endpoint
from app.schemas.endpoint import EndpointCreate, EndpointUpdate


class CRUDEndpoint(CRUDBase[Endpoint, EndpointCreate, EndpointUpdate]):
    def get_by_url(self, db: Session, *, url: str) -> Optional[Endpoint]:
        return db.query(Endpoint).filter(Endpoint.url == url).first()

    def create(self, db: Session, *, obj_in: EndpointCreate) -> Endpoint:
        db_obj = Endpoint(
            name=obj_in.name.upper(),
            url=obj_in.url.upper(),
            description=obj_in.description.upper()
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db: Session, *, db_obj: Endpoint, obj_in: Union[EndpointUpdate, Dict[str, Any]]) -> Endpoint:
        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "name" in update_data:
            uppercase_name = str(update_data["name"]).upper()

            update_data["name"] = uppercase_name

        if "url" in update_data:
            uppercase_url = str(update_data["url"]).upper()

            update_data["url"] = uppercase_url

        return super().update(db, db_obj=db_obj, obj_in=update_data)


endpoint = CRUDEndpoint(Endpoint)