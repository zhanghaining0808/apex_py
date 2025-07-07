from sqlmodel import SQLModel, Session, create_engine, select
from models.weapon import Weapon
from models.hero import Hero
from data.hero import heros
from data.weapon import weapons

postgres_url = "postgresql://zhanghn:040808@localhost:5432/apex_db"
engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    create_db_and_tables()
    with Session(engine) as session:
        statement = select(Hero)
        is_existing = session.exec(statement).all()

        if not is_existing:
            session.add_all(heros)
            session.commit()
            print(f"数据表没有数据，录入数据成功, 录入{len(heros)}个英雄")
        else:
            hero_names = [hero.name for hero in heros]
            print(f"已存在英雄:{hero_names} 数据")


def init_db():
    create_db_and_tables()
    with Session(engine) as session:
        statement = select(Weapon)
        is_existing = session.exec(statement).all()

        if not is_existing:
            session.add_all(weapons)
            session.commit()
            print(f"数据表没有数据，录入数据成功, 录入{len(weapons)}把武器")
        else:
            weapon_names = [weapon.name for weapon in weapon_names]
            print(f"已存在武器:{weapon_names} 数据")
