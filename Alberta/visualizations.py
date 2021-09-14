import os
import sys
import sqlite3 as sql 
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
    data = []
    for entry in output:
        new_value = list(entry)
        temp = new_value[0].split(" ")
        new_value[0] = temp[0]
        data.append(new_value)
        #print(new_value)
    data.sort(key=takeFist)
    for age in data:
        print(age[0])
    return cursor
    #active vs overall

def takeFist(elem):
    return elem[0][0]
    

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