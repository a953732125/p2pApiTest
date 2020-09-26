from bs4 import BeautifulSoup
from parameterized import parameterized
from api.account_api import GetAccountApi
from api.reg_login_api import LoginRegApi
import unittest, requests, logging

from utils import common_assert


class TestGetAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.session = requests.Session()
        cls.get_account = GetAccountApi(cls.session)
        cls.login = LoginRegApi(cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def test01_approve_real_name(self):
        self.login.login('18123456789', 'admin123')
        real_name = '张三'
        card_id = '330102199003073332'
        r = self.get_account.approve_real_name(real_name, card_id)
        print(r.json())

    def test02_approve_info(self):
        self.login.login('18123456789', 'admin123')
        r = self.get_account.get_approve_info()
        print(r.json())

