import requests
import pandas as pd
import sqlite3
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime 


#PIPELINE

def extract(url,table_attribs):
    df = pd.DataFrame(columns=table_attribs)
    html = requests.get(url).text
    data = BeautifulSoup(html,'html.parser')

    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')

    for row in rows:

        col = row.find_all('td')

        if len(col) != 0 and row.find_all('a', href = True):
            if col[2].text.strip() != '—':
              data_dict = {table_attribs[0] : col[0].text.strip(),
                     table_attribs[1] : col[2].text.strip(),
                     }
            else:
                 pass
            
            df1 = pd.DataFrame(data_dict,index=[0])
            df = pd.concat([df,df1], ignore_index=True)
    
    return df


def transform(df):
    Columns = df.columns
    column = Columns[1]

    df[column] = df[column].str.replace(',','').astype(float)
    df[column] = np.round(df[column]/1000,2)
    df.rename(columns = {column : 'GDP_USD_billions'},inplace = True)

    return df


def load_to_csv(df,csv_path):

    df.to_csv(csv_path)

def load_to_db(df,sql_connection,table_name):

    df.to_sql(table_name,sql_connection,if_exists='replace', index = False)

def run_query(query_statement,sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
   

def log_progress(message): 
    log_file = "log_file.txt"
    timestamp_format = '%Y-%h-%d-%H:%M:%S' 
    now = datetime.now()
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n')


    
conn = sqlite3.connect('World_Economies.db')
table_name = 'GDP_by_country'
query= f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
csv_path = 'GDP'
table_attribs = ['Country/Territory','GSD_USD_MILLION']
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

log_progress('Preliminares completados. Inicio del proceso ETL')

df1 = extract(url,table_attribs)

log_progress('Extracción de datos completa. Inicio del proceso de transformación')

df = transform(df1)

log_progress('Transformación de datos completada. Iniciando proceso de carga')

load_to_csv(df,csv_path)

log_progress('Datos guardados en archivo CSV')

load_to_db(df,conn,table_name)

log_progress('Datos cargados en la base de datos como tabla. Ejecutar la consulta')

run_query(query,conn)

log_progress('Proceso completado.')

conn.close()