import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://ysparpwudfzsfq:16e524e58bd4a5c14809784324fdf2daffc31af93a49639ce8bd3797f4914722@ec2-3-233-43-103.compute-1.amazonaws.com:5432/d1o0q2q561psd0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'