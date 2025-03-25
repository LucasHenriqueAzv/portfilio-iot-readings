import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from os import getenv

# processando as variaveis de ambiente
load_dotenv()

# lendo dataset
dataset = pd.read_csv('./data/IOT-temp.csv')

# criando conexao com o db
postgres_password = getenv('POSTGRES_PASSWORD')
connection_string = f'postgresql://postgres:{postgres_password}@localhost:5432/postgres'
engine = create_engine(connection_string)

dados_inseridos = dataset.to_sql('temperature_readings', engine, if_exists='replace', index=False)

print(f'foram inseridos {dados_inseridos} dados')

queries_views = [
    # media de temperatura agrupada por sensor (In ou Out)
    """
    CREATE OR REPLACE VIEW avg_temp_por_local AS
    SELECT "out/in" AS sensor_location, AVG(temp) AS avg_temp
    FROM temperature_readings
    GROUP BY "out/in";
    """,
    # contagem de leituras por hora (a partir do noted_date)
    """
    CREATE OR REPLACE VIEW leituras_por_hora AS
    SELECT EXTRACT(HOUR FROM to_timestamp(noted_date, 'DD-MM-YYYY HH24:MI')) AS hora,
           COUNT(*) AS contagem
    FROM temperature_readings
    GROUP BY hora
    ORDER BY hora;
    """,
    # temperaturas max e min / dia (convertendo noted_date para formato de data)
    """
    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
    SELECT to_char(to_timestamp(noted_date, 'DD-MM-YYYY HH24:MI'), 'YYYY-MM-DD') AS data,
           MAX(temp) AS temp_max,
           MIN(temp) AS temp_min
    FROM temperature_readings
    GROUP BY data
    ORDER BY data;
    """
]

with engine.begin() as connection:
    for query in queries_views:
        connection.execute(text(query))
        print("view criada")
