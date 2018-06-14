# coding:utf8

# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as db
from tutorial import settings
from twisted.enterprise import adbapi
import pymysql.cursors
from tutorial.items import GamerankItem

class MysqlTwistedPipline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        db_pool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 异步插入
        query = self.db_pool.runInteraction(self.insert_item, item)
        query.addErrback(self.handle_error)
        return item

    def insert_item(self, cursor, item):
        insert_sql = """ insert into table3(rank, game) values(%s, %s) """
        cursor.execute(insert_sql, (item['rank'], item['game']))

    def handle_error(self, failure):
        print(failure)
