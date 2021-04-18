import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://s797lpai7wm3gucu:td9qh8rdi1e87jly@xlf3ljx3beaucz9x.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ujmuqrlhu79bpuef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
