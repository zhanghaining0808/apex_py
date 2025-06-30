from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db.db import get_session
from models.weapon import Weapon


weapon_router = APIRouter()


@weapon_router.get("/weapons")
def get_all_weapons(session: Session = Depends(get_session)):
    return session.exec(select(Weapon)).all()


@weapon_router.get("/weapons/{weapon_tag}")
def query_weapon_by_name(weapon_tag: str, session: Session = Depends(get_session)):
    find_weapon = session.exec(select(Weapon).where(Weapon.name == weapon_tag)).first()

    if not find_weapon:
        find_weapon = session.get(Weapon, weapon_tag)

    if not find_weapon:
        return {"error": "没用该武器!"}
    return find_weapon
