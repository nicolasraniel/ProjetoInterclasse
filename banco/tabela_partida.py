from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Partida, Time

def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    times_sql = select(Time)
    # 2 - Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()

    return partidas

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida, ):
    try:
        partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
        db_session.add(partida_nova)
        db_session.commit()
        flash('Partida cadastrado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")