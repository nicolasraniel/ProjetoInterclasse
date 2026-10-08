from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Jogador


def select_todos():
    # Buscar todos os times no banco
    # 1 - Montar o select
    # join(Tabela que eu quero juntar, condição=chave estrangeira igual a chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2 - Executar o select
    # usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    print(jogadores)
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())

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
