from os import times
from tokenize import group

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Jogador


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    times_sql = (
        select(Time, func.count(Jogador.id).label("jogadores"))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id))
    # 2 - Executar o select
    times = db_session.execute(times_sql).all()

    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total

print(select_quantidade_total())


def salvar(nome, turma, responsavel):
    try:
        time_novo = Time(nome=nome, turma=turma, responsavel=responsavel)
        db_session.add(time_novo)
        db_session.commit()
        flash('Time cadastrado com sucesso', 'success')
        return time_novo
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")

def select_um(id_time):
    times_sql = select(Time).where(Time.id == id_time)
    time = db_session.execute(times_sql).scalar_one_or_none()
    return time
