from api.invest_api import InvestApi
from api.reg_login_api import LoginRegApi
from api.recharge_api import RechargeApi
from api.account_api import GetAccountApi
import unittest, requests, logging, random
from utils import GetData, common_assert, clear_test_data


class TestInvestBusiness(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        clear_test_data()
        cls.session = requests.Session()
        cls.reg_login = LoginRegApi(cls.session)
        cls.account = GetAccountApi(cls.session)
        cls.recharge = RechargeApi(cls.session)
        cls.invest = InvestApi(cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def test_invest_business(self):
        r = random.random()
        phone_num = '13812345698'
        img_code = '8888'
        phone_code = '666666'
        pwd = 'admin123'
        real_name = '张三'
        card_id = '330102199003073332'
        dy_server = 'on'
        try:
            # 获取图片验证码
            self.reg_login.get_img_code(r)
            # 获取手机验证码
            self.reg_login.get_note_code(phone_num, img_code)
            # 注册
            reg = self.reg_login.register(phone_num, pwd, img_code, phone_code, dy_server)
            print(reg.json())
            # 登录
            self.reg_login.login(phone_num, pwd)
            # 实名认证
            self.account.approve_real_name(real_name, card_id)
            # 开户
            r1 = self.recharge.set_account()
            # 获取第三方
            res1 = GetData.get_html_data(r1)
            third1 = self.session.post(url=res1[0], data=res1[1])
            logging.info('第三方响应文本:{}'.format(third1.text))
            self.assertIn('OK', third1.text)
            # 获取充值验证码
            self.recharge.get_charge_verify_code(r)
            # 充值
            r2 = self.recharge.recharge('chinapnrTrust', '2000', 'reForm', '8888')
            # 第三方
            res2 = GetData.get_html_data(r2)
            third2 = self.session.post(url=res2[0], data=res2[1])
            logging.info('第三方响应文本:{}'.format(third2.text))
            self.assertIn('OK', third2.text)
            # 投资产品详情成功
            self.invest.get_invest_detail(842)
            # 投资
            r3 = self.invest.invest(842, 1000)
            # 第三方
            res3 = GetData.get_html_data(r3)
            third3 = self.session.post(url=res3[0], data=res3[1])
            logging.info('第三方响应文本:{}'.format(third3.text))
            self.assertIn('OK', third3.text)
        except Exception as e:
            logging.error(e)
            raise
