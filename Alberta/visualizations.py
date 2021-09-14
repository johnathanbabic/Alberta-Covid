import os
import sqlite3 as sql
import sys
import numpy as np
import matplotlib.pyplot as plt



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
    sequence = ["Under","1-4","5-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]
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
    recovery = []
    deathRate = []
    death = []

    for item in data_dict:
        active.append(data_dict[item][0])
        totals.append(data_dict[item][1])
        recovery.append((data_dict[item][2])*100)
        deathRate.append((data_dict[item][-1])*100)

    for i in range(0,len(totals)):
        value = (deathRate[i])/100 * totals[i]
        death.append(value)
    

    plt.figure(figsize=(18,10),tight_layout=True)
    plt.subplot(3,2,1)
    plt.bar(labels,active)
    plt.title("Active Cases by Age Group")
    plt.ylabel("Number of Cases")
    plt.xlabel("Age group (years)")
    plt.ylim([0,5000])

    plt.subplot(3,2,2)
    plt.bar(labels,totals)
    plt.title("Total Cases by Age Group")
    plt.ylabel("Number of Cases")
    plt.xlabel("Age group (years)")
    plt.ylim([0,75000])

    plt.subplot(3,2,3)
    plt.bar(labels,recovery)
    plt.title("Recovery Rate by Age Group")
    plt.ylabel("Rate (%)")
    plt.xlabel("Age group (years)")
    plt.ylim([0,100])

    plt.subplot(3,2,4)
    plt.bar(labels,deathRate)
    plt.title("Death Rate by Age Group")
    plt.ylabel("Rate (%)")
    plt.xlabel("Age group (years)")
    plt.ylim([0,30])

    plt.subplot(3,2,5)
    plt.bar(labels,death)
    plt.title("Deaths by Age Group")
    plt.ylabel("Number of Deaths")
    plt.xlabel("Age group (years)")
    plt.ylim([0,2000])

    plt.show()
    
    return cursor




def rates_by_age(cursor):
    # revocery and death rates ascending
    pass

def rates_by_location(cursor):
    pass


def main():
    con, cur = connect_to_db()
    cur = cases_by_age(cur)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()
