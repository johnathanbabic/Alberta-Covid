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

def by_age(cursor):
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

def by_gender(cursor):
    script = "select * from genders;"
    cursor.execute(script)
    output = cursor.fetchall()
    genders =[]
    totalCases = []
    activeCases = []
    recoveryRate = []
    deathRate = []
    deaths = []
    for item in output:
        values = list(item)
        if values[0] != "Unknown":
            genders.append(values[0])
            activeCases.append(values[1])
            totalCases.append(values[2])
            recoveryRate.append(values[3]*100)
            deathRate.append(values[4]*100)
            deaths.append(values[2]*values[4])

    plt.figure(figsize=(18,10),tight_layout=True)
    plt.subplot(3,2,1)
    plt.bar(genders,activeCases)
    plt.title("Active Cases by Gender")
    plt.ylabel("Number of Cases")
    plt.xlabel("Gender")
    plt.ylim([0,15000])

    plt.subplot(3,2,2)
    plt.bar(genders,totalCases)
    plt.title("Total Cases by Gender")
    plt.ylabel("Number of Cases")
    plt.xlabel("Gender")
    plt.ylim([0,150000])

    plt.subplot(3,2,3)
    plt.bar(genders,recoveryRate)
    plt.title("Recovery Rate by Gender")
    plt.ylabel("Rate (%)")
    plt.xlabel("Gender")
    plt.ylim([0,100])

    plt.subplot(3,2,4)
    plt.bar(genders,deathRate)
    plt.title("Death Rate by Gender")
    plt.ylabel("Rate (%)")
    plt.xlabel("Gender")
    plt.ylim([0,2.5])

    plt.subplot(3,2,5)
    plt.bar(genders,deaths)
    plt.title("Deaths by Gender")
    plt.ylabel("Number of Deaths")
    plt.xlabel("Gender")
    plt.ylim([0,2000])

    plt.show()

    return cursor

def by_location(cursor):
    script = "select * from locations;"
    cursor.execute(script)
    output = cursor.fetchall()
    locations =[]
    totalCases = []
    activeCases = []
    recoveryRate = []
    deathRate = []
    deaths = []
    for item in output:
        values = list(item)
        if values[0] != "Unknown":
            locations.append(values[0])
            activeCases.append(values[1])
            totalCases.append(values[2])
            recoveryRate.append(values[3]*100)
            deathRate.append(values[4]*100)
            deaths.append(values[2]*values[4])

    plt.figure(figsize=(18,10),tight_layout=True)
    plt.subplot(3,2,1)
    plt.bar(locations,activeCases)
    plt.title("Active Cases by Location")
    plt.ylabel("Number of Cases")
    plt.xlabel("Location")
    plt.ylim([0,10000])

    plt.subplot(3,2,2)
    plt.bar(locations,totalCases)
    plt.title("Total Cases by Location")
    plt.ylabel("Number of Cases")
    plt.xlabel("Location")
    plt.ylim([0,150000])

    plt.subplot(3,2,3)
    plt.bar(locations,recoveryRate)
    plt.title("Recovery Rate by Location")
    plt.ylabel("Rate (%)")
    plt.xlabel("Location")
    plt.ylim([0,100])

    plt.subplot(3,2,4)
    plt.bar(locations,deathRate)
    plt.title("Death Rate by Location")
    plt.ylabel("Rate (%)")
    plt.xlabel("Location")
    plt.ylim([0,2.5])

    plt.subplot(3,2,5)
    plt.bar(locations,deaths)
    plt.title("Deaths by Location")
    plt.ylabel("Number of Deaths")
    plt.xlabel("Location")
    plt.ylim([0,2000])

    plt.show()

    return cursor

def vaccinations(cursor):
    script = "select * from vacinations;"
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

def main():
    con, cur = connect_to_db()
    #cur = by_age(cur)
    #cur = by_gender(cur)
    cur = by_location(cur)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()
