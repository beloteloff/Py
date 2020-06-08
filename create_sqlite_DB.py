from argparse import ArgumentParser
import sqlite3
from sqlalchemy import create_engine

connector = sqlite3.connect('actions.db')   # create a connection object - a new sqlite database
##c = connector.cursor()
#function which load data from file to table in sqlite DB
def loader(location):    
    source = pd.read_csv('~/actions.csv', encoding="utf-8")
    print(source.describe())
    source.to_sql(name="Choice", con=connector, if_exists="replace",index=False)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-f", dest="location", action="store", required=True, type=str, help="format of input file is csv or txt")
    loader(parser.parse_args().location)
