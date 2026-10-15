from os import times

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # Buscar todos os times no banco
    # 1 - Montar o select
    times_sql = select(Time)
    # 2 - Executar o select
    times = tabela_time.select_quantidade_total()
    jogadores_sql = select(Jogador)
    jogadores = tabela_jogador.select_quantidade_total()
    partidas_sql = select(Partida)
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores_sql = select(Jogador)
    # 2 - Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return render_template("jogadores.html", jogadores=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa", "").strip()
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id", "").strip()

        # 2 - Verificar se foi digitado
        if not nome:
            flash('Digite o nome do jogador', 'error')
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash('Digite o numero da camisa', 'error')
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash('Digite a posição do jogador', 'error')
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash('Digite o time', 'error')
            return redirect(url_for("novo_jogador"))

        # 3 - Salvar no banco
        tabela_jogador.salvar(nome, numero_camisa, posicao, time_id)

    jogadores = tabela_jogador.select_todos()
    times = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    print(times)
    return render_template("times.html", times=times)
@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        jogadores_ids = request.form.getlist("jogadores")

        # 2 - Verificar se foi digitado
        if not nome:
            flash('Digite o nome do time', 'error')
            return redirect(url_for("novo_time"))
        if not turma:
            flash('Digite a turma', 'error')
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash('Digite o responsável', 'error')
            return redirect(url_for("novo_time"))

        # 3 - Salvar no banco
        time = tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        if jogadores_ids:
            for jogador_id in jogadores_ids:
                jogador = tabela_jogador.select_um(jogador_id)
                jogador.time_id = time.id
                db_session.add(jogador)
                db_session.commit()


    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()
    return render_template("times.html", times=times, jogadores=jogadores)



@app.route("/time/<id_time>")
def detalhes_time(id_time):
    time = tabela_time.select_um(int(id_time))
    jogadores = tabela_jogador.select_por_time(int(id_time))
    partidas = tabela_partida.select_por_time(int(id_time))
    return render_template(
        "time_detalhes.html",
        time=time,
        jogadores=jogadores,
        qtd_jogadores=len(jogadores),
        partidas=partidas,
        qtd_partidas=len(partidas)
    )

@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todas_partidas()
    print(partidas)
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        if not time_casa_id:
            flash('Digite o time da casa', 'error')
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash('Digite o time visitante', 'error')
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash('Digite o total de gols do time da casa', 'error')
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash('Digite o total de gols do time visitante', 'error')
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash('Digite a data da partida', 'error')
            return redirect(url_for("nova_partida"))


        # 3 - verificar se os times são iguais
        if time_casa_id == time_visitante_id:
            flash('selecione times diferentes', 'error')
            return render_template("partidas.html")


        # 4 - Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todas_partidas()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
