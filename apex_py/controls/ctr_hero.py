from fastapi import Depends
from fastapi import APIRouter
from sqlmodel import Session, select
from db.db import get_session
from models.hero import Hero

hero_router = APIRouter()
# 创建一个FastAPI的子路由对象,后续所有路径操作都会挂载到/heros前缀下


@hero_router.get("/heros")
def get_all_heros(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()


@hero_router.get("/heros/{hero_tag}")
def query_hero_by_name(hero_tag: str, session: Session = Depends(get_session)):
    find_hero = session.exec(select(Hero).where(Hero.name == hero_tag)).first()

    if not find_hero:
        find_hero = session.get(Hero, hero_tag)

    if not find_hero:
        return {"error": "没有该英雄!"}
    return find_hero


# @hero_router.get("/heros/by_id/{hero_id}")
# def query_hero_by_id(hero_id: str, session: Session = Depends(get_session)):
#     find_hero = session.get(Hero, hero_id)
#     if not find_hero:
#         return {"error": "没有该英雄!"}
#     return find_hero


# @hero_router.get("/heros/by_name/{hero_name}")
# def query_hero_by_name(hero_name: str, session: Session = Depends(get_session)):
#     find_hero = session.exec(select(Hero).where(Hero.name == hero_name)).first()
#     if not find_hero:
#         return {"error": "没有该英雄!"}
#     return find_hero
