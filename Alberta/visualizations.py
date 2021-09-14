import os
import sqlite3 as sql
import sys

import matplotlib.pyplot as plt
import numpy as np


def connect_to_db():
    # This will function will open the database if it 
    # exists. Otherwise it will end the program if db
    # is not found.
    if os.path.exists("covid.db"):
        try: 
            con = sql.connect("covid.db")
            cur = con.cursor() 
            con.commit()
        
        except:
            print("ERROR: Connection to database")
            con.close()
            exit()
    else:
        print("ERROR: No database found")
        exit()

    return con,cur

def cases_by_age(cursor):
    script = "select * from age_groups;"
    cursor.execute(script)
    output = cursor.fetchall()
    sequence = ["Under","1-4","5-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+","Unknown"]
    data = []
    for entry in output:
        new_value = list(entry)
        temp = new_value[0].split(" ")
        new_value[0] = temp[0]
        data.append(new_value)

    total = 0  
    totalActive = 0
     
    data_dict = {}
    for age in sequence:
        for entry in data:
            if entry[0] == age:
                data_dict[age] = entry[1:]
                total += entry[2]
                totalActive += entry[1]
    
    

    labels = list(data_dict.keys())
    active = []
    totals = []

    for item in data_dict:
        active.append((int(data_dict[item][0])/totalActive)*100)
        totals.append((int(data_dict[item][1])/total)*100)
    
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rect1 = ax.bar(x - width/2, active, width, label="Active Cases")
    rect2 = ax.bar(x - width/2, totals, width, label="Total Cases")

    ax.set_ylabel("Percentage")
    ax.set_title("Active and Total Cases by Age Group")
    ax.set_xticks(x)
    ax.legend()

    ax.bar_label(rect1,padding=3)
    ax.bar_label(rect2,padding=3)

    fig.tight_layout()

    plt.show()

    recovery = []
    death = []

    
    
    return cursor



    #active vs overall


def rates_by_age(cursor):
    # revocery and death rates ascending
    pass


def main():
    con, cur = connect_to_db()
    cur = cases_by_age(cur)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()
