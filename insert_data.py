import pandas as pd
from sqlalchemy import create_engine
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