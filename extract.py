import csv
import sqlite3
file = open("data.csv", encoding="utf8")
reader = csv.reader(file)
count = 0
for row in reader:
    if count > 0:
        bib = row[16]
        if bib=='':
            bib = row[17]
        if bib=='':
            bib="None"


        task = (bib,str(count))
        print(bib)
        sql = ''' UPDATE videos SET about = ? WHERE ID = ? '''
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        
        count += 1
    else:
        count += 1

file.close()
