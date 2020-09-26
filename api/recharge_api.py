import requests, app


class RechargeApi:
    def __init__(self, session):
        self.session = session
        self._set_account_url = app.BASE_URL + '/trust/trust/register'
        self._get_recharge_code_url = app.BASE_URL + '/common/public/verifycode/{}'
        self._recharge_url = app.BASE_URL + '/trust/trust/recharge'

    # 开户接口
    def set_account(self):
        return self.session.post(url=self._set_account_url)

    def get_charge_verify_code(self, r):
        return self.session.post(url=self._get_recharge_code_url.format(r))

    def recharge(self, paymentType, amount, formStr, valicode):
        form = {
            "paymentType": paymentType,
            "amount": amount,
            "formStr": formStr,
            "valicode": valicode
        }
        return self.session.post(url=self._recharge_url, data=form)
