from sklearn.neighbors import DistanceMetric
df=pd.concat([uni_geo[['Name','lat','long']],locators[['Name','lat','long']],...,df_apple[['Name','lat','long']]]).reset_index(drop=True)

dist = DistanceMetric.get_metric('haversine')
D = dist.pairwise(np.radians(df_base[['lat','long']]), np.radians(df[['lat','long']])) * 6371

def zoning(ds):
    if ds < 300:
        return 1
    elif ds < 600 and ds >=300:
        return 2
    elif ds < 1200 and ds >=600:
        return 3
    elif ds < 1500 and ds >=1200:
        return 4
    elif ds < 3000 and ds >=1500:
        return 5
    elif ds >=3000:
        return 6
    else:
        return 0
full_df=pd.DataFrame(D, columns=df.Sklad.unique(),index=df_base.Sklad.unique()).T
full_df=full_df.stack().reset_index(level=1, name='dist').rename(columns={'level_1':'Name_base'})[['dist','Name_base']].rename_axis('Name').reset_index()
full_df=full_df[full_df['dist']<6].reset_index(drop=True)
full_df['dist']=full_df['dist']*1000
full_df['zone'] = full_df['dist'].apply(zoning)
full_df 
