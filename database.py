import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db_info = config['DB']

conn = pymysql.connect(
    host=db_info['HOST'],
    user=db_info['USER'],
    password=db_info['PASSWORD'],
    db=db_info['DB'],
    charset='utf8'
)