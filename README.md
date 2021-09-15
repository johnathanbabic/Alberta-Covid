This is a project that will extract data from the Goverment of Alberta website and put into database file.

createCovoidDB.py is the program that will extract the data from the website and download the file into your current directory. Once downloaded, it will put the data into a database file using the schema in the tables.sql file. This program uses pandas to open the files as well as sqlite3 to import the data into the db file.

visualization.py will extract the data from the database file and use them to make visualizations on various covid statistics based on age, gender, and location. This progam utalizes matploblib in order to create the visualzations.

NOTE: This is only for Alberta covid data.

Property of Johnathan Babic
