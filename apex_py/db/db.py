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
        all_heros = session.exec(statement).all()

        if not all_heros:
            session.add_all(heros)
            session.commit()
            print(f"数据表没有数据，录入数据成功, 录入{len(heros)}个英雄")

        miss_heros = []
        for hero in heros:
            if all_heros.count(hero) <= 0:
                session.add(hero)
                session.commit()
                miss_heros.append(hero)
        if len(miss_heros) > 0:
            print(
                f"数据表检测到遗漏数据，现已同步缺失{[hero.name for hero in miss_heros]}英雄"
            )

        else:
            print(f"数据表存在数据，已有{[hero.name for hero in all_heros]}这些英雄")

    # 武器的代码也照抄改一下
    with Session(engine) as session:
        statement = select(Weapon)
        all_weapons = session.exec(statement).all()

        if not all_weapons:
            session.add_all(weapons)
            session.commit()
            print(f"数据表没有数据，录入数据成功, 录入{len(weapons)}把武器")
        else:
            print(
                f"数据表存在数据，已有{[weapons.name for weapons in all_weapons]}这些武器"
            )
