import os, json
from bs4 import BeautifulSoup
import pymysql, logging.handlers, app


# 状态码/status/description
def common_assert(self, res, desc=None, status_code=200, status=200):  # 公共断言方法
    self.assertEqual(status_code, res.status_code)
    if status:
        self.assertEqual(status, res.json()['status'])
    if desc:
        self.assertIn(desc, res.json()['description'])


# 数据操作工具类
class DBUtils:
    __conn = None

    @classmethod
    def get_conn(cls):
        if cls.__conn is None:
            cls.__conn = pymysql.connect('52.83.144.39', 'root', 'Itcast_p2p_20191228',
                                         'czbk_member', port=3306, charset='utf8')
        return cls.__conn

    @classmethod
    def execute_sql(cls, sql):
        cursor = cls.get_conn().cursor()
        cursor.execute(sql)
        try:
            if sql.lower().split(' ')[0] == 'select':  # 对查询语句的处理
                return cursor.fetchall()  # 获取查询的所有数据
            else:
                cls.get_conn().commit()  # 如果不是查询语句且没有异常就提交事务
                return cursor.rowcount  # 返回影响的行数

        except:
            cls.get_conn().rollback()  # 数据异常,事务回滚
        finally:
            cls.close_conn(cursor)

    @classmethod
    def close_conn(cls, cursor=None):
        if cursor:
            cursor.close()
        if cls.__conn:
            cls.__conn.close()
            cls.__conn = None


# 日志读取工具类
class GetLogger:
    _logger = None

    @classmethod
    def init_log(cls):
        if cls._logger is None:
            # 创建日志器
            cls._logger = logging.getLogger()
            cls._logger.setLevel(logging.INFO)
            # 创建文件处理器
            file_path = app.DIR_NAME + os.sep + 'log' + os.sep + 'p2p.log'
            file_handler = logging.handlers.TimedRotatingFileHandler(filename=file_path, when='midnight',
                                                                     interval=1, backupCount=15, encoding='utf-8')
            # 创建控制台处理器
            stream_handler = logging.StreamHandler()
            # 创建格式化器
            fmt = "%(asctime)s %(levelname)s [%(name)s][%(filename)s(%(funcName)s:%(lineno)d)]- %(message)s"
            formatter = logging.Formatter(fmt)
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            # 添加到日志器上
            cls._logger.addHandler(file_handler)
            cls._logger.addHandler(stream_handler)
        return cls._logger


# 数据读取类
class GetData:
    file_path = app.DIR_NAME + os.sep + 'data'

    # 读取json数据
    @classmethod
    def get_json_data(cls, file_name, case_name):
        data_list = []
        with open(cls.file_path + os.sep + file_name, 'r', encoding='utf-8')as f:
            data = json.load(f).get(case_name)
        for i in data:
            data_list.append(tuple(i.values())[1:])  # 获取数据中字典的value值,通过切片从第二个开始获取数据
        return data_list

    # 读取html页面的数据
    @classmethod
    def get_html_data(cls, response):
        html = response.json()['description']['form']
        soup = BeautifulSoup(html, 'html.parser')  # 解析html
        url = soup.form['action']
        labs = soup.find_all('input')  # 获取所有input标签的内容
        html_data = {}
        for i in labs:
            html_data[i['name']] = i['value']
        return url, html_data


# 清除数据方法
def clear_test_data():
    # 清除登录日志表
    sql = """delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id WHERE m.phone in ("13812345698", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtils.execute_sql(sql)
    print("sql执行结果：{}".format(result))
    logging.info("sql执行结果：{}".format(result))

    # 清除会员信息表
    sql = """DELETE i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ("13812345698", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtils.execute_sql(sql)
    print("sql执行结果：{}".format(result))
    logging.info("sql执行结果：{}".format(result))

    # 清除会员主表
    sql = """delete from mb_member where phone in ("13812345698", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtils.execute_sql(sql)
    print("sql执行结果：{}".format(result))
    logging.info("sql执行结果：{}".format(result))

    # 清除注册日志表
    sql = """DELETE from mb_member_register_log where phone in ("13812345698", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtils.execute_sql(sql)
    print("sql执行结果：{}".format(result))
    logging.info("sql执行结果：{}".format(result))


if __name__ == '__main__':
    x = GetData.get_json_data('reg_login.json', 'img_code')
    print(x)
    # data_list = []
    # data = GetData.get_json_data('reg_login.json', 'img_code')
    # for i in data:
    #     data_list.append(tuple(i.values())[1:])  # 获取数据中字典的value值,通过切片从第二个开始获取数据
    # print(data_list)
    # clear_test_data()
