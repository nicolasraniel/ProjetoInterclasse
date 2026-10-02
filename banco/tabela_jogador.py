from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Jogador


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    jogadores_sql = select(Jogador)
    # 2 - Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    print(jogadores)
    return jogadores

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        jogador_novo = Jogador(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=int(time_id))
        db_session.add(jogador_novo)
        db_session.commit()
        flash('Jogador cadastrado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", 'error')
        print(f"Erro: {e}")
