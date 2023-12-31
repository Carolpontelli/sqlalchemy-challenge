# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

# Criar uma aplicação Flask
app = Flask(__name__)

# Conectar ao banco de dados SQLite
engine = create_engine("sqlite:///hawaii.sqlite")

# Refletir o banco de dados em classes ORM
Base = automap_base()
Base.prepare(engine, reflect=True)

# Referências para as tabelas
Station = Base.classes.station
Measurement = Base.classes.measurement

# Criar uma sessão
session = Session(engine)

# Definir rotas

@app.route("/")
def home():
    return (
        f"Bem-vindo à Climate Analysis API!<br/>"
        f"Rotas Disponíveis:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calcular a data de um ano atrás a partir da última data no banco de dados
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Consultar dados de precipitação
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Converter resultados para dicionário
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Consultar lista de estações
    results = session.query(Station.station).all()

    # Converter resultados para uma lista
    station_list = list(np.ravel(results))

    return jsonify(station_list)

# Rotas semelhantes para outras análises...

if __name__ == "__main__":
    app.run(debug=True)