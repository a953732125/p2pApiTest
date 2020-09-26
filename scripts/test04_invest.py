from api.invest_api import InvestApi
from api.reg_login_api import LoginRegApi
import unittest, requests, logging
from utils import GetData, common_assert


class TestInvest(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session = requests.Session()
        login = LoginRegApi(cls.session)
        cls.invest = InvestApi(cls.session)
        login.login('18123456789', 'admin123')
        logging.info("获取session:{}".format(cls.session))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        logging.info('关闭session{}'.format(cls.session))

    def test01_get_invest_detail(self):
        r = self.invest.get_invest_detail(842)
        logging.info("响应数据:{}".format(r.json()))
        try:
            self.assertEqual('842', r.json()['data']['loan_info']['id'])
        except Exception as e:
            logging.error(e)
            raise

    def test02_invest(self):
        r = self.invest.invest(842, 1000)
        res = GetData.get_html_data(r)
        r2 = self.session.post(url=res[0], data=res[1])
        logging.info('响应数据:{}'.format(r2.text))
        try:
            self.assertIn('OK', r2.text)
        except Exception as e:
            logging.error(e)
            raise

    def test03_get_invest_list(self):
        r = self.invest.get_invest_list(1, 'tender')
        logging.info('响应数据:{}'.format(r.json()))
        try:
            self.assertEqual('842', r.json()['items'][0]['loan_id'])
        except Exception as e:
            logging.error(e)
            raise
