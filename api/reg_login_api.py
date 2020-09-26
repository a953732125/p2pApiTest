import requests, app
import logging


class LoginRegApi:
    def __init__(self, session):
        self.session = session
        self._img_code_url = app.BASE_URL + '/common/public/verifycode1/{}'
        self._note_code_url = app.BASE_URL + '/member/public/sendSms'
        self._register_url = app.BASE_URL + '/member/public/reg'
        self._login_url = app.BASE_URL + '/member/public/login'
        self._is_login_url = app.BASE_URL + '/member/public/islogin'

    # 获取图片验证码
    def get_img_code(self, r):
        logging.info("获取图片验证码")
        return self.session.get(url=self._img_code_url.format(r))

    # 获取手机验证码
    def get_note_code(self, phone_num, img_code):
        form = {
            "phone": phone_num,
            "imgVerifyCode": img_code,
            "type": "reg"
        }
        logging.info("获取手机验证码,请求url:{},请求数据:{}".format(self._note_code_url, form))
        return self.session.post(url=self._note_code_url, data=form)

    # 注册
    def register(self, phone_num, pwd, img_code, phone_code, dy_server='on', invite_phone=''):
        reg_form = {
            "phone": phone_num,
            "password": pwd,
            "verifycode": img_code,
            "phone_code": phone_code,
            "dy_server": dy_server,
            "invite_phone": invite_phone
        }
        logging.info("调用注册接口,请求url:{},请求数据:{}".format(self._register_url, reg_form))
        return self.session.post(url=self._register_url, data=reg_form)

    # 登录
    def login(self, phone, pwd):
        login_form = {
            "keywords": phone,
            "password": pwd
        }
        logging.info("调用登录接口,请求url:{},请求数据:{}".format(self._login_url, login_form))
        return self.session.post(url=self._login_url, data=login_form)

    # 是否登录
    def is_login(self):
        logging.info('调用登录状态接口,请求url:{}'.format(self._is_login_url))
        return self.session.post(url=self._is_login_url)


if __name__ == '__main__':
    session = requests.Session()
    get_code = LoginRegApi(session)
    res1 = get_code.get_img_code('0.5')
    res2 = get_code.get_note_code('18123456789', '8888')
    res3 = get_code.register('18123456789', 'admin123', '8888', '666666')
    res4 = get_code.is_login()
    print(res3.json())
    print(res4.json())
    session.close()
