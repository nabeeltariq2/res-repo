import os
from sqlalchemy import *








DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@nabeeltariq2.cgbqvatgwbqb.us-east-1.rds.amazonaws.com/nabeeltariq2?charset=utf8')


# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:sesame@localhost/newmovietweetings?charset=utf8')
