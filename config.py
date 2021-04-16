import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_PATH = "/home/liliangbin/audio/"
    SERVER_URLS = 'http://localhost:5000/'

    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVE_DATABASE_URL') or 'mysql+pymysql://ft_ssr:ft_ssr@big.forcebing.top:3305/ft_ssr?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                       'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
