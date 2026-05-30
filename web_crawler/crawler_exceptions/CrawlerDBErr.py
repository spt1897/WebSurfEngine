class CrawlerDBErr(Exception):
    pass

#redis pool connection errors:
class RedisPoolErr(CrawlerDBErr):
    pass
#mysql pool connection errors:
class MysqlPoolErr(CrawlerDBErr):
    pass
