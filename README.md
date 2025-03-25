# Projeto: Pipeline de Dados com IoT e Docker

## Estrutura de Arquivos

 

- **.env-example**  
  Contém as variáveis de ambiente, incluindo a senha do PostgreSQL (`POSTGRES_PASSWORD`).

- **.gitignore**  
  Define arquivos/pastas que não devem ser commitados (como `.env` e `.venv`).

- **docker-compose.yml**  
  Arquivo de configuração Docker para subir o contêiner do PostgreSQL.

- **insert_data.py**  
  Script responsável por:
  1. Ler o dataset `IOT-temp.csv`.
  2. Inserir os dados na tabela `temperature_readings` no banco PostgreSQL.
  3. Criar as views necessárias para análise.

- **dashboard.py**  
  Aplicação em Streamlit que carrega as views do banco de dados e exibe gráficos interativos usando Plotly.

- **requirements.txt**  
  Lista de dependências Python necessárias para o projeto (Pandas, Psycopg2, SQLAlchemy, Streamlit, Plotly, python-dotenv, etc.).

- **data/IOT-temp.csv**  
  Arquivo CSV contendo as leituras de temperatura (retirado do Kaggle).

---

## Pré-requisitos

1. **Docker** instalado e em execução.
2. **Python 3.8+** instalado.
3. **Bibliotecas** listadas em `requirements.txt` instaladas (caso vá rodar localmente fora do contêiner).

---

## Passo a Passo de Configuração e Execução

### 1. Clonar o Repositório

```
git clone https://github.com/LucasHenriqueAzv/portfilio-iot-readings.git
cd portfolio-iot-readings
```


### 2. Configurar as Variáveis de Ambiente

Substitua o nome do arquivo `.env-example` por `.env` para poder carregar as variáveis de ambiente.


### 3. Subir o Contêiner do PostgreSQL

Utilize o **Docker Compose** para iniciar o serviço:

```
docker-compose up -d
``` 

Isso fará o download da imagem oficial do PostgreSQL e criará um contêiner chamado `postgres-iot`, expondo a porta `5432`.


### 4. Criar e Popular o Banco de Dados

1.  **Crie e ative um ambiente virtual (venv)**:
    
    ```
    python -m venv .venv source .venv/bin/activate
    ```
    
    _No Windows, use:_
    ```
    .venv\Scripts\activate 
    ```
    
2.  **Instale as dependências**:
	```
    pip install -r requirements.txt
    ```
 
    
3.  **Execute o script de inserção** no banco:
    ```
    python insert_data.py
    ```
    
    -   Este script fará a leitura do arquivo `IOT-temp.csv`, criará (ou substituirá) a tabela `temperature_readings` e executará as queries de criação das views.
        

### 5. Executar o Dashboard

Por fim, rode o aplicativo Streamlit que exibirá os gráficos:
```
streamlit run dashboard.py
```

Acesse o endereço que aparecerá no terminal (`http://localhost:8501`) para visualizar o dashboard.

----------

## Visão Geral do Dashboard

A aplicação Streamlit (`dashboard.py`) gera três gráficos principais:

1.  **Média de Temperatura por Local (Interno/Externo)**
    
2.  **Leituras por Hora do Dia**
    
3.  **Temperaturas Máximas e Mínimas por Dia**
    

### Exemplos de Capturas de Tela

#### 1. Média de Temperatura por Local (Interno/Externo)
![Gráfico de Média de Temperatura por Local](https://github.com/LucasHenriqueAzv/portfilio-iot-readings/blob/ebc45551eb9c31399bbb8fba86c0d8989e0fa108/images/media_temperatura_io.png?raw=true "Média de Temperatura por Local")

#### 2. Leituras por Hora do Dia
![Gráfico de Leituras por Hora do Dia](https://github.com/LucasHenriqueAzv/portfilio-iot-readings/blob/ebc45551eb9c31399bbb8fba86c0d8989e0fa108/images/leituras_hora.png?raw=true "Leituras por Hora do Dia")

#### 3. Temperaturas Máximas e Mínimas por Dia
![Gráfico de Temperaturas Máximas e Mínimas por Diacal](https://github.com/LucasHenriqueAzv/portfilio-iot-readings/blob/ebc45551eb9c31399bbb8fba86c0d8989e0fa108/images/temperatus_maximas_minimas.png?raw=true "Temperaturas Máximas e Mínimas por Dia")

----------

## Explicação das Views SQL

O script `insert_data.py` cria três views no banco de dados PostgreSQL:

1.  **avg_temp_por_local**

    `CREATE  OR REPLACE VIEW avg_temp_por_local AS  SELECT "out/in" AS sensor_location, AVG(temp) AS avg_temp FROM temperature_readings GROUP  BY "out/in";` 
    
    -   **Objetivo**: Calcular a média de temperatura agrupada pelo local do sensor (“In” ou “Out”).
        
3.  **leituras_por_hora**
    
    `CREATE  OR REPLACE VIEW leituras_por_hora AS  SELECT  EXTRACT(HOUR  FROM to_timestamp(noted_date, 'DD-MM-YYYY HH24:MI')) AS hora, COUNT(*) AS contagem FROM temperature_readings GROUP  BY hora ORDER  BY hora;` 
    
    -   **Objetivo**: Contar quantas leituras foram registradas em cada hora do dia, auxiliando na análise de períodos de maior/menor atividade de registro.
        
4.  **temp_max_min_por_dia**
    
    `CREATE  OR REPLACE VIEW temp_max_min_por_dia AS  SELECT to_char(to_timestamp(noted_date, 'DD-MM-YYYY HH24:MI'), 'YYYY-MM-DD') AS data, MAX(temp) AS temp_max, MIN(temp) AS temp_min FROM temperature_readings GROUP  BY data ORDER  BY data;` 
    
    -   **Objetivo**: Exibir, para cada dia, as temperaturas máxima e mínima registradas, permitindo analisar a amplitude térmica diária ao longo do período.
        

----------

## Possíveis Insights Obtidos

-   **Média de Temperatura por Local (Interno x Externo)**
    
    -   Há uma diferença notável (cerca de 6 °C) entre o sensor interno (“In”) e o externo (“Out”).
        
    -   Ainda assim, se a temperatura interna estiver na faixa de 30 °C+ (considerando graus Celsius), é pouco confortável para um escritório. Isso sugere a possibilidade de pouca eficiência de refrigeração interna ou de condições climáticas extremas.
        
-   **Contagem de Leituras por Hora do Dia**
    
    -   Observa-se um pico de temperatura por volta das 14 h, que coincide com o horário de maior calor em muitos locais, quando o sol já aqueceu o ambiente.
        
    -   Às 4 h, os valores tendem a ser mais baixos, pois é um período noturno em que o solo e o ambiente já perderam o calor acumulado durante o dia.
        
-   **Temperaturas Máximas e Mínimas por Dia**
    
    -   De julho a setembro, as leituras de temperatura mínima e máxima são mais próximas. Isso sugere menor variação diária, possivelmente um período de verão/começo de outono, quando a amplitude térmica não é tão acentuada.
        
    -   A partir de meados de setembro até dezembro, a diferença entre as leituras de mínima e máxima aumenta, o que pode indicar uma transição de estação (outono para inverno, no hemisfério norte). As temperaturas mínimas caem mais rapidamente do que as máximas, resultando em maior amplitude térmica diária.
