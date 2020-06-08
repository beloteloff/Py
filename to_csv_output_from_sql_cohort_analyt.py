import cx_Oracle

import csv
import os
os.environ["NLS_LANG"] = ".UTF8"
os.environ["NLS_LANG"] = "Russian.AL32UTF8"#"American_America.AL32UTF8" ".UTF8"

dsnStr = cx_Oracle.makedsn("s34.birt.localka", "1231", "bird")

conn = cx_Oracle.connect(user="USEROK", password="top_secret", dsn=dsnStr,encoding='utf-8')
curs = conn.cursor()

printHeader = True 
outputFile = open('cohort_analytics.csv','w') # 'wb'
output = csv.writer(outputFile, delimiter ='|', lineterminator='\n')

sql='''with store as
(SELECT distinct storeid,store FROM db.store_base),
cohorts as (SELECT min(TO_CHAR(dato,'YYYY-MM')) as mindate,carnumb as users
FROM db.sales WHERE dato >= TO_DATE('2011-01-01','YYYY-MM-DD') 
AND dato < TO_DATE('2019-04-01','YYYY-MM-DD') GROUP BY carnumb)
SELECT TO_CHAR(dato,'YYYY-MM') as Period,store, mindate as Cohort, COUNT(distinct carnumb) as Quant_clnt
FROM db.ret INNER JOIN store ON store.storeid=ret.storeid
INNER JOIN cohorts ON cohorts.users=ret.carnumb
WHERE dato >= TO_DATE('2011-01-01','YYYY-MM-DD') AND dato < TO_DATE('2019-04-01','YYYY-MM-DD')
AND b2b_flag=0 GROUP BY TO_CHAR(dato,'YYYY-MM'),store, mindate '''

curs.execute(sql)

if printHeader:
    cols = []
    for col in curs.description:
        cols.append(col[0])
    output.writerow(cols)

for row_data in curs:
    #print(type(str(row_data)))
    output.writerow(row_data)


outputFile.close()
