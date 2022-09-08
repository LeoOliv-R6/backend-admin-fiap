import logging
from sqlalchemy.orm import Session
from app import schemas, crud
from app.core.config import settings

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    if settings.EMAIL_FIRST_SUPERADMIN:
        administrator = crud.administrator.get_by_email(db, email=settings.EMAIL_FIRST_SUPERADMIN)

        if not administrator:
            role = crud.role.get_by_name_and_level(db, name="API", level=1)

            if not role:
                role_in = schemas.RoleCreate(
                    name="API",
                    level=1,
                    description="SUPER ADMINISTRATOR OF APPLICATION ECOSYSTEM"
                )

                role = crud.role.create(db, obj_in=role_in)

            administrator_in = schemas.AdministratorCreate(
                name=settings.NAME_FIRST_SUPERADMIN,
                email=settings.EMAIL_FIRST_SUPERADMIN,
                password=settings.PASS_FIRST_SUPERADMIN,
                document=settings.DOCUMENT_FIRST_SUPERADMIN,
                role_id=role.id
            )

            administrator = crud.administrator.create(db, obj_in=administrator_in)

        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.EMAIL_FIRST_SUPERADMIN} already exists. "
            )

    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@beplix.com"
        )