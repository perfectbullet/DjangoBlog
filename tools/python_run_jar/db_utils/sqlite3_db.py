import os
from os.path import join
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import JarConf, NginxConf

DB_PATH = join(os.getcwd(), 'db1.db')
engine = create_engine("sqlite:///{}".format(DB_PATH), echo=True)


def save_jar_conf(jar_conf: dict):
    """
    保存 jar包配置信息
    @param jar_conf: 
    @return: 
    """
    with Session(engine) as session:
        jar_conf = JarConf(
            jar_name=jar_conf['jar_name'],
            conf_name=jar_conf['jar_name'],
            fullname=jar_conf['fullname'],
            ser_port=jar_conf['ser_port']
        )
        session.add(jar_conf)
        session.commit()


if __name__ == '__main__':
    dbEngine = create_engine('sqlite:////home/stephen/db1.db')  # ensure this is the correct path for the sqlite file.
    #
    # #3.- Read data with pandas
    # pd.read_sql('select * from test',dbEngine)
    #
    # #4.- I also want to add a new table from a dataframe in sqlite (a small one)
    #
    # df_todb.to_sql(name = 'newTable',con= dbEngine, index=False, if_exists='replace')
