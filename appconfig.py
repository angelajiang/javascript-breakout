class Config(object):
    DEBUG = False
    TESTING = False
    AVERAGESFILE = 'logs/average_hits'
    TABLEFILE = 'tables/current/small_table'
    TABLEDIR = 'tables/train'
    PERIOD = 1000000
    WRITECOUNT = 1050

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    GETAVERAGES = False
    GETRESULTS = True
    AVERAGESFILE = 'logs/average_hits_test'
    RESULTSFILE = 'logs/results'
    TABLEFILE = 'tables/current/small_table_test'
    TABLEDIR = 'tables/test'
    PERIOD = 50000

class DevConfig(Config):
    DEBUG = True
    AVERAGESFILE = 'logs/average_hits_dev'
    TABLEFILE = 'tables/current/small_table_debug'
    TABLEDIR = 'tables/debug'
