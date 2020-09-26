from api.recharge_api import RechargeApi
from api.reg_login_api import LoginRegApi
import unittest, requests, random, logging

from utils import GetData, common_assert

phone = '18123456789'
pwd = 'admin123'


class TestRecharge(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session = requests.Session()
        cls.login = LoginRegApi(cls.session)
        cls.recharge = RechargeApi(cls.session)
        cls.login.login(phone, pwd)  # 登录

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    # 开户测试
    def test01_set_account(self):
        r = self.recharge.set_account()
        print(r.text)
        common_assert(self, r, status_code=200, status=200, desc='form')
        h = GetData.get_html_data(r)
        r2 = self.session.post(url=h[0], data=h[1])
        common_assert(self, r2, status_code=200, status=None)

    # 充值验证码测试
    def test02_recharge_code(self):
        r = self.recharge.get_charge_verify_code(random.random())
        logging.info('响应数据:{}'.format(r.text))
        try:
            common_assert(self, r, status=None)
        except Exception as e:
            logging.error(e)
            raise

    # 充值测试
    def test03_recharge(self):
        self.recharge.get_charge_verify_code(random.random())
        r = self.recharge.recharge('chinapnrTrust', '500', 'reForm', '8888')
        logging.info('响应:{}'.format(r.json()))
        common_assert(self, r, desc='form')
        h = GetData.get_html_data(r)
        r2 = self.session.post(url=h[0], data=h[1])  # 第三方开户
        try:
            common_assert(self, r2, status=None)
        except Exception as e:
            logging.error(e)
            raise
