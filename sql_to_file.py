import cx_Oracle,os
os.environ["NLS_LANG"] = "Russian.AL32UTF8" #"American_America.AL32UTF8" ".UTF8"

dsnStr = cx_Oracle.makedsn("b42.brand.local", "1521", "birg")

connection = cx_Oracle.connect(user="user", password="Pass", dsn=dsnStr,encoding='utf-8')
curs = connection.cursor()

sql = ''' SELECT * FROM db.table WHERE rownum < 3 '''
curs.execute(sql)

with open('output_file.csv', 'w') as f:
    f.write('|'.join(str(col[0]) for col in curs.description) + "\n")
    for row in curs:
        #print(''.join(str(row[9]) ))
        print(*row ,sep='|', file=f) # get all elements from tuple
        
connection.close()
f.close()
