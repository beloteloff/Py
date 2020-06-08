import urllib2
from bs4 import BeautifulSoup
strana=['ru']
#,'ua','az','am','by','ge','kz','kg','lt','lv','md','tj','tm','uz','ee','ww']
f=open("Megogo_content_list.csv",'w')
f.write('page\tstrana\tfile_url\ttitle_rus\ttitle_en\tcategorie\trating_kinopoisk\timdb\tinfo_year\tcountry\tdistribution_vod_type\n')
for k in range(0,1):
    u1='http://xml.megogo.net/assets/files/'+strana[k]+'/all_mgg.xml'
    #u2='http://xml.megogo.net/assets/files/'+strana[k]+'/all_embed_mgg.xml'
    #u3='http://xml.megogo.net/assets/files/'+strana[k]+'/music_mgg.xml'
    #u4='http://xml.megogo.net/assets/files/'+strana[k]+'/music_embed_mgg.xml'
    #u5='http://xml.megogo.net/assets/files/'+strana[k]+'/tv_mgg.xml'
    #u6='http://xml.megogo.net/assets/files/'+strana[k]+'/tv_embed_mgg.xml '
    u=[u1]
#,u2,u3,u4,u5,u6]
    for j in range(0, 1):
        page=urllib2.urlopen(u[j])
        soup=BeautifulSoup(page,"html.parser")
        titles=soup.findAll('object')
        i=0
        for el in titles:
            object_id=titles[i].get('page').encode('utf-8')
            title_rus=titles[i].get('title').encode('utf-8')
            title_en=titles[i].get('title_en').encode('utf-8')
            categorie=titles[i].get('categories').encode('utf-8')
            rating_kinopoisk=(titles[i].findAll('ratings'))[0].get('kinopoisk').encode('utf-8')
            imdb=(titles[i].findAll('ratings'))[0].get('imdb').encode('utf-8')
            info_year=(titles[i].findAll('info'))[0].get('year').encode('utf-8')
            country=(titles[i].findAll('info'))[0].get('country').encode('utf-8')
            distribution_vod_type=titles[i].get('vod').encode('utf-8')
            f.write(object_id+'\t'+strana[k]+'\t'+u[j]+'\t'+title_rus+'\t'+title_en+'\t'+categorie+'\t'+rating_kinopoisk+'\t'+imdb+'\t'+info_year+'\t'+country+'\t'+distribution_vod_type+'\n')
            i=i+1
f.close()
