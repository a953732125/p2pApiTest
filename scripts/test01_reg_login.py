import time
from parameterized import parameterized
from api.reg_login_api import LoginRegApi
import unittest, requests, random, logging
from utils import common_assert, GetData, clear_test_data


def json_data(file_name, case_name):
    return GetData.get_json_data(file_name, case_name)


class TestRegLogin(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session = requests.Session()
        cls.login_reg = LoginRegApi(cls.session)
        logging.info('获取session对象:{}'.format(cls.session))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        logging.info('关闭session:{}'.format(cls.session))

    # 1.图片验证码
    @parameterized.expand(json_data('reg_login.json', 'img_code'))
    def test01_img_code(self, r, status_code):
        r1 = self.login_reg.get_img_code(r)
        logging.info('获取图片验证码response对象')
        try:
            common_assert(self, r1, status_code=status_code, status=None)
        except Exception as e:
            logging.error(e)
            raise

    # # 获取验证码成功:随机数为整数
    # def test01_2_img_code(self):
    #     r = self.login_reg.get_img_code(random.randint(100000, 999999))
    #     logging.info('获取图片验证码response对象:{}'.format(r))
    #     try:
    #         common_assert(self, r, status=None)
    #     except Exception as e:
    #         logging.error(e)
    #
    # # 获取验证码失败:随机数为字符串
    # def test01_3_img_code(self):
    #     x = random.sample('qwertyuiopasdfghjklzxcvbnm', 8)
    #     r = self.login_reg.get_img_code(''.join(x))
    #     logging.info('获取图片验证码response对象:{}'.format(r))
    #     try:
    #         common_assert(self, r, status=None)
    #     except Exception as e:
    #         logging.error(e)
    #
    # 获取验证码失败:随机数为空
    # def test01_4_img_code(self):
    #     r = self.login_reg.get_img_code('')
    #     logging.info('获取图片验证码response对象:{}'.format(r))
    #     try:
    #         common_assert(self, r, status=None)
    #     except Exception as e:
    #         logging.error(e)
    #         raise

    # 2.手机验证码
    @parameterized.expand(json_data('reg_login.json', 'phone_code'))
    def test02_phone_code(self, phone, img_code, status_code, status, exp):
        self.login_reg.get_img_code(random.random())
        r = self.login_reg.get_note_code(phone, img_code)
        logging.info('获取手机验证码response对象')
        try:
            common_assert(self, r, status_code=status_code, status=status, desc=exp)
        except Exception as e:
            logging.error(e)
            raise

    clear_test_data()

    # 3.注册
    @parameterized.expand(json_data('reg_login.json', 'register'))
    def test03_reg(self, phone, pwd, img_code, phone_code, dy_server, invite_phone, status_code, status, exp):
        self.login_reg.get_img_code(random.random())
        self.login_reg.get_note_code(phone, img_code)
        r = self.login_reg.register(phone, pwd, img_code, phone_code, dy_server=dy_server, invite_phone=invite_phone)
        logging.info('获取注册response对象:{}'.format(r.text))
        try:
            common_assert(self, r, status_code=status_code, status=status, desc=exp)
        except Exception as e:
            logging.error(e)

    # 4.登录
    # @parameterized.expand(json_data('reg_login.json', 'login'))
    # def test04_login(self, phone, pwd, status_code, status, exp):
    #     r = self.login_reg.login(phone, pwd)
    #     logging.info('获取登录response对象:{}'.format(r.text))
    #     if 'error' in pwd:
    #         n = 0
    #         while n < 2:
    #             r = self.login_reg.login(phone, pwd)
    #             logging.info('获取登录response对象:{}'.format(r.text))
    #             n += 1
    #         time.sleep(60)
    #         r = self.login_reg.login('18123456789', 'admin123')
    #         logging.info('获取登录response对象:{}'.format(r.text))
    #     try:
    #         common_assert(self, r, status_code=status_code, status=status, desc=exp)
    #     except Exception as e:
    #         logging.error(e)
    #         raise

    # 5.是否登录
    def test05_is_login(self):
        phone = '18123456789'
        pwd = 'admin123'
        self.login_reg.login(phone, pwd)
        r = self.login_reg.is_login()
        logging.info('获取判定登录状态response对象:{}'.format(r.text))
        common_assert(self, r, desc='OK')
