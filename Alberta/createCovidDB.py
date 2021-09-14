# This program will take the data that is provided from the 
# Government of Alberta and put the data into .db file.
# This data will later be used to create data visualizations. 

import os
import sys
import requests
import sqlite3 as sql
import pandas as pd

def get_data_from_web(url):
    file_name = get_filename(url)
    if os.path.exists(file_name):
        os.remove(file_name)
        download_file(url)
    else:
        download_file(url)

def download_file(url):
    local_filename = get_filename(url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

def get_filename(url):
    local_filename = url.split('/')[-1]
    return local_filename

def connect_to_db():
    try: 
        con = sql.connect("covid.db")
        cur = con.cursor() 
        f = open("tables.sql","r")
        contents = f.read()
        cur.executescript(contents)
        con.commit()
    
    except:
        print("ERROR: Connection to database")
        con.close()
        exit()

    return con,cur

def get_data():
    covid = pd.read_csv("covid-19-alberta-statistics-data.csv")
    vaccines = pd.read_csv("lga-coverage.csv")
    return covid,vaccines

def clean_data(covid, vaccines):
    covid = covid.drop(columns=["Unnamed: 0","Date reported","Case type"])
    #print(covid)

    vaccines = vaccines.drop(columns=["Local Code","Local Name","Zone Name"])
    #print(vaccines)
    return covid, vaccines

def insert_covid_data(covid, cursor):
    age_groups = covid["Age group"].unique()
    locations = covid["Alberta Health Services Zone"].unique()
    genders = covid["Gender"].unique()

    for group in age_groups:
        data = covid.loc[covid["Age group"] == group]
        active_cases,total_cases, recovery_rate, death_rate = get_group_count(data, group)
        #print("Age Group:",group,"| Active cases:",active_cases,"| Total cases:",total_cases,"| Recovery %:",recovery_rate,"| Death %:",death_rate,"\n")
    
        insert_data = "insert into age_groups values (?, ?, ?, ?, ?);"
        cursor.execute(insert_data, (group, int(active_cases), int(total_cases), float(recovery_rate), float(death_rate)))
    
    for location in locations:
        data = covid.loc[covid["Alberta Health Services Zone"] == location]
        active_cases,total_cases, recovery_rate, death_rate = get_group_count(data, location)
        #print("Location:",location,"| Active cases:",active_cases,"| Total cases:",total_cases,"| Recovery %:",recovery_rate,"| Death %:",death_rate,"\n")

        insert_data = "insert into locations values (?, ?, ?, ?, ?);"
        cursor.execute(insert_data, (location, int(active_cases), int(total_cases), float(recovery_rate), float(death_rate)))

    for gender in genders:
        data = covid.loc[covid["Gender"] == gender]
        active_cases,total_cases, recovery_rate, death_rate = get_group_count(data, gender)
        #print("Gender:",gender,"| Active cases:",active_cases,"| Total cases:",total_cases,"| Recovery %:",recovery_rate,"| Death %:",death_rate,"\n")
        
        insert_data = "insert into genders values (?, ?, ?, ?, ?);"
        cursor.execute(insert_data, (gender, int(active_cases), int(total_cases), float(recovery_rate), float(death_rate)))
    return cursor

def get_group_count(data, group):
    active_cases = data.loc[data["Case status"] == "Active"].count()["Case status"]
    total_cases = data["Case status"].count()
    recovered = data.loc[data["Case status"] == "Recovered"].count()["Case status"]
    died = data.loc[data["Case status"] == "Died"].count()["Case status"]
    non_current = data.loc[data["Case status"] != "Active"].count()["Case status"]
    recovery_rate = recovered/non_current
    death_rate = died/non_current

    return active_cases,total_cases, recovery_rate, death_rate

def insert_vaccine_data(vaccines, cursor):
    age_groups = vaccines["Age Group"].unique()
    for group in age_groups:
        partial = float(vaccines.loc[vaccines["Age Group"] == group]["Alberta: percent of population who received at least one dose"].unique())/100
        full = float(vaccines.loc[vaccines["Age Group"] == group]["Alberta: percent of population fully immunized"].unique())/100
        #print(group, partial, full)

        insert_data = "insert into vacinations values (?, ?, ?);"
        cursor.execute(insert_data, (group,partial,full))
    return cursor


def main():
    get_data_from_web("https://www.alberta.ca/data/stats/covid-19-alberta-statistics-data.csv")
    get_data_from_web("https://www.alberta.ca/data/stats/lga-coverage.csv")
    con,cur = connect_to_db()
    covid,vaccines = get_data()
    covid, vaccines = clean_data(covid, vaccines)
    cur = insert_covid_data(covid, cur)
    cur = insert_vaccine_data(vaccines, cur)
    con.commit()
    con.close()

main()