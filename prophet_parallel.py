# coding: utf-8

import pandas as pd,numpy as np, matplotlib, sys,cx_Oracle,csv#os
pd.plotting.register_matplotlib_converters()

pd.set_option('display.max_columns', 77)
#os.environ["NLS_LANG"] = ".UTF8"

#reload(sys)
#sys.setdefaultencoding('utf-8')

logo=pd.read_csv('Login.csv')
##new version need .strip()
name=logo['user'].to_string(index=False).strip()
passport=logo['password'].to_string(index=False).strip()

dsnStr = cx_Oracle.makedsn("b78.parfum3.locale", "1521", "wird")
conn = cx_Oracle.connect(user="%s" % name, password="%s" % passport, dsn=dsnStr,encoding='utf-8')

df_shopsWOptAll=pd.read_sql ('''
SELECT .... FROM table.db''' , con=conn)
df_shopsWOptAll.to_csv('amount_sales_all.csv',index=False,sep='|')
df_shopsWOptAll=pd.read_csv('amount_sales_all.csv',sep='|',usecols=['SKLAD','Y','DS'])

conn.close()

print ("+------------------------------------------------+\n" + "|              SELECT WAS FINISHED               |\n+------------------------------------------------+")


ny = pd.DataFrame({
  'holiday': 'new_year',
  'ds': pd.to_datetime(['2017-12-31', '2016-12-31', '2015-12-31','2014-12-31','2013-12-31','2018-12-31','2019-12-31']),
  'lower_window': 0,
  'upper_window': 8,
})

shorty=pd.DataFrame({
  'holiday': 'short_holy',
    'ds': pd.to_datetime(['2013-02-23','2014-02-23','2015-02-23','2016-02-23','2017-02-23','2018-02-23','2019-02-23',
'2013-03-08','2014-03-08', '2015-03-08','2016-03-08','2017-03-08','2018-03-08','2019-03-08']),
  'lower_window': -1,
  'upper_window': 0,
})

cs=pd.DataFrame({
  'holiday': 'crazy_sale',
    'ds': pd.to_datetime(['2018-01-17','2019-01-17','2018-08-01','2019-08-01']),
  'lower_window': 0,
  'upper_window': 15,
})

sd=pd.DataFrame({
  'holiday': 'sms2day',
    'ds': pd.to_datetime(['2019-02-13','2018-02-13','2018-02-22','2019-02-22','2019-05-24','2018-05-25','2019-06-09','2018-06-09','2019-06-21','2018-06-22','2018-11-23','2019-11-23']),
  'lower_window': 0,
  'upper_window': 1,
})


import matplotlib

holy = pd.concat((cs, sd, ny, shorty)).sort_values(by='ds',ascending=True,kind='mergesort').reset_index(drop=True)
print(holy)
from math import exp
from fbprophet import Prophet
#get_ipython().magic('matplotlib inline')
##from fbprophet.diagnostics import cross_validation

def sms_happy(ds):
    date = pd.to_datetime(ds)
    if (((date.month == 10 and (date.day==13 or date.day==14)) or (date.month == 9 and (date.day==8 or date.day==9)) or (date.month == 12 and (date.day==8 or date.day==9))) and date.year == 2017) or ((date.month == 12 and (date.day==7 or date.day==8)) and date.year == 2018) or ((date.month == 12 and (date.day==6 or date.day==7)) and date.year == 2019):
        return 1
    else:
        return 0

holydays = pd.read_csv('dates.csv')


listok=[]
##listok2=[]
UniqueNames = df_shopsWOptAll.SKLAD.unique()
##print(UniqueNames)
DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}
for key in DataFrameDict.keys():
    globals()['df%s' % (key)]= df_shopsWOptAll[['DS','SKLAD','Y']][:][df_shopsWOptAll.SKLAD == key]
    ##listok2.append('df%s' % (key))
    listok.append(globals()['df%s' % (key)])

print (UniqueNames)
def dayNameFromWeekday(weekday):
    if weekday == 0:
        return "понедельник"
    if weekday == 1:
        return "вторник"
    if weekday == 2:
        return "среда"
    if weekday == 3:
        return "четверг"
    if weekday == 4:
        return "пятница"
    if weekday == 5:
        return "суббота"
    if weekday == 6:
        return "воскресенье"


from calendar import weekday, day_name

##drop counter, coz is's not loop
print ("+------------------------------------------------+\n" + "|            Before function is started          |\n+------------------------------------------------+")

def calculation (df):
    column=np.array_str(df['SKLAD'].unique()).replace("['","").replace("']","")
    
    ##fil_Sales = open("PredictionChecks_parallel_30min_%s.csv" % str(column), "w")
    logi = open("logi.csv", "a+")
    ##counter=0 
    splity=df[['DS','Y']]
    ##print (column)
    splity.columns= ['ds', 'yold']
    splity = splity.query('yold!=0')
    std_yyy=splity['yold'].std()
    ##splity['MA']=pd.rolling_mean(splity['yold'],window=7,min_periods=1)
    splity['MA']=splity['yold'].rolling(7).mean()
    not_in=splity[~splity['ds'].isin(holydays['ds'])]
    in_intersection=splity[splity['ds'].isin(holydays['ds'])]
    not_in['y'] = not_in['yold']
    
    in_intersection['y']=in_intersection['yold']
    frames = [not_in,in_intersection]
        
    fin_df = pd.concat(frames).sort_values(by='ds',ascending=True,kind='mergesort')
    fin_df['y'] = np.log(fin_df['y'])
    fin_df=fin_df[['ds','y','yold']]
    ##fin_df['ds']=pd.to_datetime(fin_df['ds'])
    fin_df['sms_happy'] = fin_df['ds'].apply(sms_happy)
    
    filtr=fin_df['ds'][~fin_df['yold'].isnull()].min()
    fin_df=fin_df[fin_df['ds']>=filtr]
    ##counter = counter+1
    history = fin_df[fin_df['y'].notnull()].copy()
    history['ds']=history['ds'].astype(str)
    ##history['ds']=pd.to_datetime(history['ds'].dt.strftime('%Y-%m-%d'))
    if (history.shape[0] > 30) and (history['ds'].max() > '2019-10-01'):
        shop_prophet = Prophet(holidays=sd).add_regressor('sms_happy',prior_scale=1,standardize=False).fit(fin_df)
        shop_future = shop_prophet.make_future_dataframe(periods=62,freq = "D")        
        
        fin_df['ds']=pd.to_datetime(fin_df['ds'])
        shop_future['sms_happy'] = shop_future['ds'].apply(sms_happy)
        shop_future=pd.concat([pd.merge(shop_future,fin_df,on=['ds','sms_happy']),shop_future[~shop_future['ds'].isin(splity['ds'])]], sort=True)##.sort_values(by='ds',ascending=True,kind='mergesort')
        
        shop_future['SKLAD']=column

        ##########################
              
        shop_forecast = shop_prophet.predict(shop_future)
        
        #shop_prophet.plot_components(shop_forecast)
        #matplotlib.pyplot.gcf().savefig('Seasonality for shop %s.png' % (str(column)))
        #matplotlib.pyplot.close('all')
        shop_predict=shop_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        shop_predict=pd.merge(shop_predict,fin_df,on=['ds'],how='left')
                
        shop_predict['y'] = np.exp(shop_predict['y'])
        shop_predict['yhat'] = np.exp(shop_predict['yhat'])
        shop_predict['yhat_lower'] = np.exp(shop_predict['yhat_lower'])
        shop_predict['yhat_upper'] = np.exp(shop_predict['yhat_upper'])
        
        ##shop_predict['delta'] = 100-shop_predict['yhat']/shop_predict['yold']*100
        fin_df['y'] = np.exp(fin_df['y'])
        global shop_predict_upd
        shop_predict_upd=shop_predict[['ds','yhat','y','yold', 'yhat_lower', 'yhat_upper']].copy()
        shop_predict_upd['SKLAD']=column
        
        ##shop_predict_upd[shop_predict_upd['ds']>='2018-10-01'].to_csv(fil_Sales,index=False,encoding='utf8',sep=';')

        ##fin_df[['ds','y','yold']].plot(figsize=(12,6),title='Shop purchase in %s ' % (str(column)),x='ds')
        ##shop_predict[['ds','yhat','y']].plot(figsize=(12,6),title="Purchase prediction for shop %s " % (str(column)),x='ds')
        ##matplotlib.pyplot.gcf().savefig('Purchase prediction for shop %s.png' % (str(column)))
        ##print(', '.join(shop_forecast.columns))
        shopmetrics = shop_predict.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(fin_df.set_index('ds'))
        lenn1 = round(shopmetrics['yold'].dropna(axis=0, how='all').shape[0])
        ##lenn = round(shopmetrics['yhat'].shape[0])
        shopmetrics=shopmetrics[shopmetrics['y'] >0].tail(72)
        shopmetrics['e'] = shopmetrics['y'] - shopmetrics['yhat']
        shopmetrics['e_lower'] = shopmetrics['y'] - shopmetrics['yhat_lower']
        shopmetrics['e_upper'] = shopmetrics['y'] - shopmetrics['yhat_upper']
        shopmetrics['p'] = 100*shopmetrics['e']/shopmetrics['y']
        shopmetrics['p_lower'] = 100*shopmetrics['e_lower']/shopmetrics['y']
        shopmetrics['p_upper'] = 100*shopmetrics['e_upper']/shopmetrics['y']
    
        logi.write ("\n" + str(column) + "\n" + 'MAPE lower' + " " + str(np.mean(abs(shopmetrics['p_lower']))) + '\n')
        logi.write ('MAE lower' + " " + str(np.mean(abs(shopmetrics['e_lower']))) + '\n')
        logi.write ('\tMAPE' + " " + str(np.mean(abs(shopmetrics['p']))) + '\n')
        logi.write ('\tMAE' + " " + str(np.mean(abs(shopmetrics['e']))) + '\n')
        logi.write ('MAPE upper' + " " + str(np.mean(abs(shopmetrics['p_upper']))) + '\n')
        logi.write ('MAE upper' + " " + str(np.mean(abs(shopmetrics['e_upper'])) ) + '\n')
        
        
        std_y = shopmetrics['y'].std()
        std_yhat = shopmetrics['yhat'].std()
       
        logi.write ("Initial data std" + " " + str(std_y) + '\n')
        logi.write ("Approximating data std" + " " + str(std_yhat) + '\n')
        logi.write (str(lenn1) + '\n')

        logi.write (str(shopmetrics.tail(72))  + '\n'  + '\n')
        logi.close()
        ##fil_Sales.close()
        ##print ("Shop " + str(column) + "finished" )
        
    return (shop_predict_upd[(shop_predict_upd['ds']>='2019-11-01') & (shop_predict_upd['ds']< '2020-01-01')]) 


from multiprocessing import Pool
if __name__ == "__main__":
    ##maper=open("maper.csv", "a+")
    pool = Pool(11)
    df = pd.concat(pool.map(calculation, listok)) #.drop_duplicates().reset_index(drop=True)
    ##maper.write (str(pool.map(calculation, listok)))
    ##logi.close()
    df.to_csv('All_predo_.csv',index=False,encoding='utf8',sep='|')
    pool.close()
    pool.join()
    print ("finish")
