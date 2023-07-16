import os
from os.path import join
from sqlalchemy import create_engine


DB_PATH = join(os.getcwd(), 'db1.db')
engine = create_engine("sqlite:///{}".format(DB_PATH), echo=True)

if __name__ == '__main__':

    dbEngine = create_engine('sqlite:////home/stephen/db1.db') # ensure this is the correct path for the sqlite file.
    #
    # #3.- Read data with pandas
    # pd.read_sql('select * from test',dbEngine)
    #
    # #4.- I also want to add a new table from a dataframe in sqlite (a small one)
    #
    # df_todb.to_sql(name = 'newTable',con= dbEngine, index=False, if_exists='replace')