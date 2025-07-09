from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlmodel import Session, select
from db.db import get_session
from models.hero import Hero

# 创建一个FastAPI的子路由对象,后续所有路径操作都会挂载到/heros前缀下
hero_router = APIRouter(prefix="/heros")

# 就按这个写吧，方便一点
SessionDep = Annotated[Session, Depends(get_session)]

# query一般表示查询的意思，我这里给你修改一下原来的http api路由路径，这样的话语义更明显


@hero_router.get("/query")
@hero_router.post("/query")
def get_all_heros(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()


@hero_router.get("/query/{hero_tag}")
@hero_router.post("/query/{hero_tag}")
def query_hero_by_name(hero_tag: str, session: SessionDep):
    find_hero = session.exec(select(Hero).where(Hero.name == hero_tag)).first()

    if not find_hero:
        find_hero = session.get(Hero, hero_tag)

    if not find_hero:
        return {"error": "没有该英雄!"}
    return find_hero


@hero_router.post("/add")
def add_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@hero_router.post("/delete/{hero_tag}")
def delete_hero(hero_tag: str, session: SessionDep):
    # 实现方法有很多，我这里决定根据类型来判断，你也可以实现你自己想的其他的也行
    # 懂了吗？懂了 还有一个问题
    find_hero = None

    if hero_tag.isdigit():
        find_hero = session.exec(select(Hero).where(Hero.id == hero_tag)).first()
    else:
        find_hero = session.exec(select(Hero).where(Hero.name == hero_tag)).first()

    if not find_hero:
        return {"error": "没有该英雄!"}

    session.delete(find_hero)
    session.commit()
    return find_hero


# @hero_router.post("/update/{hero_tag}")
# def update_hero_by_name(hero_tag: Hero, session: SessionDep):
#     pass


# @hero_router.get("/by_id/{hero_id}")
# def query_hero_by_id(hero_id: str, session: SessionDep):
#     find_hero = session.get(Hero, hero_id)
#     if not find_hero:
#         return {"error": "没有该英雄!"}
#     return find_hero


# @hero_router.get("/by_name/{hero_name}")
# def query_hero_by_name(hero_name: str, session: SessionDep):
#     find_hero = session.exec(select(Hero).where(Hero.name == hero_name)).first()
#     if not find_hero:
#         return {"error": "没有该英雄!"}
#     return find_hero
