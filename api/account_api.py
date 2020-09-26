import requests, app


class GetAccountApi:
    def __init__(self, session):
        self.session = session
        self.approve_real_name_url = app.BASE_URL + '/member/realname/approverealname'
        self.get_approve_url = app.BASE_URL + '/member/member/getapprove'

    # 实名认证
    def approve_real_name(self, real_name, card_id):
        approve_form = {
            "realname": real_name,
            "card_id": card_id
        }
        return self.session.post(url=self.approve_real_name_url, data=approve_form, files={"x": "y"})

    # 获取认证信息
    def get_approve_info(self):
        return self.session.post(url=self.get_approve_url)
