import logging

import requests

import app


class InvestApi:
    def __init__(self, session):
        self.session = session
        self._invest_detail_url = app.BASE_URL + '/common/loan/loaninfo'
        self._invest_url = app.BASE_URL + '/trust/trust/tender'
        self._invest_list_url = app.BASE_URL + '/loan/tender/mytenderlist'

    # 获取投资详情
    def get_invest_detail(self, ids):
        body = {
            "id": ids
        }
        logging.info('获取投资详情请求url:{},请求数据:{}'.format(self._invest_detail_url, body))
        return self.session.post(url=self._invest_detail_url, data=body)

    # 投资
    def invest(self, ids, amount):
        body = {
            "id": ids,
            "depositCertificate": -1,
            "amount": amount
        }
        logging.info('投资请求url:{},请求数据:{}'.format(self._invest_url, body))
        return self.session.post(url=self._invest_url, data=body)

    # 获取投资列表
    def get_invest_list(self, page, status):
        body = {
            "page": page,
            "status": status
        }
        logging.info('获取投资列表请求url:{},请求数据:{}'.format(self._invest_list_url, body))
        return self.session.post(url=self._invest_list_url, data=body)
