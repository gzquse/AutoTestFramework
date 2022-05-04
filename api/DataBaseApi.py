# -*- coding:utf-8 -*-
"""
模块描述:
  数据库操作类
作者：Sniper.ZH
"""
import pymysql
import commons.Config as config
from commons.Logger import logger


# ORM
class DataBaseApi:
    def __init__(self):
        self.conn = pymysql.connect(
            host=config.get_config('database.host'),
            user=config.get_config('database.user'),
            password=config.get_config('database.pass'),
            db=config.get_config('database.dbname'),
            charset="utf8mb4",
        )

    def queryMaxId(self):
        cursor = self.conn.cursor()
        sql = "select max(id) from order_info"
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        self.conn.commit()
        return res[0]

    def clearTestData(self, maxid):
        cursor = self.conn.cursor()
        sql = f"delete from order_info where id > {maxid}"
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        logger.info("数据清理完成.")

    def queryOrderById(self, order_id):
        cursor = self.conn.cursor()
        sql = f"select * from order_info where id = {order_id}"
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        self.conn.commit()
        return res

    def queryOrderCount(self, params):
        cursor = self.conn.cursor()
        where_str = ""
        if 'order_dep' in params:
            where_str += " and dep = '{}'".format(params['order_dep'])
        if 'order_date' in params:
            where_str += " and date = '{}'".format(params['order_date'])
        if 'order_type' in params:
            where_str += " and type = '{}'".format(params['order_type'])
        sql = f"select count(*) from order_info where status='0'{where_str}"
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        self.conn.commit()
        return res[0]


if __name__ == '__main__':
    dba = DataBaseApi()
    print(dba.conn)
