import pymssql
import configparser
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='Dao.log',
                    filemode='a')


class Dao(object):
    def __init__(self):
        try:
            self.__conf = configparser.ConfigParser()
            # path = os.path.join(os.path.split(os.getcwd())[0], 'config.conf')
            path = os.path.join(os.getcwd(), 'config.conf')  # 启动APP.py使用这个
            logging.debug(path)
            self.__conf.read(path)
            logging.debug(self.__conf.get('mssql', 'host'))
            self.__conn = pymssql.connect(host=self.__conf.get('mssql', 'host'),
                                          user=self.__conf.get(
                                              'mssql', 'user'),
                                          password=self.__conf.get(
                                              'mssql', 'password'),
                                          database=self.__conf.get(
                                              'mssql', 'database'),
                                          charset='utf8')
            self.__cursor = self.__conn.cursor()
        except Exception as e:
            logging.error(e)

    def select(self, sql):
        try:
            self.__cursor.execute(sql)
            rows = self.__cursor.fetchall()
            self.__conn.close()
            return rows
        except Exception as e:
            logging.error(e)

    def procedures(self, proc, parameter):
        try:
            self.__cursor.callproc(proc, parameter)
            rows = []
            for row in self.__cursor:
                rows.append(row)
            self.__conn.close()
            return rows
        except Exception as e:
            logging.error(e)
    # 删除表格中的数据参数为表名和条件
    def delect(self,table,pre):
        try:
            sql='delete from '+table+' '+pre
            self.__cursor.execute(sql)
            self.__conn.commit()
            self.__conn.close()
            return True
        except Exception as ex:
            logging.error(ex)
            return False
# ccc = Dao()
