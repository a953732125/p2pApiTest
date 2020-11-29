# # 导包
# from bs4 import BeautifulSoup
# # 解析html对象
# bs1 = BeautifulSoup("h", "html.parser")
# # 使用对象
# # 1. 获取整个title标签
# print(bs1.title)
# # 2. 获取标签名
# print(bs1.title.name)
# # 3. 获取文字
# print(bs1.title.string)
# # 4. 获取属性
# print(bs1.p.get("id"))  # print(bs1.p["id"])
# # 5. 批量找元素
# for a in bs1.find_all("a"):
#     print(a.get("href"), a.string)
import unittest,requests

from lib.EncryptUtil import EncryptUtil


class TestMobile(unittest.TestCase):

    def setUp(self) -> None:
        self.sesion = requests.session()

    def test01(self):
        """
            需求：对p2p移动端登录请求
        """
        url = "http://mobile-p2p-test.itheima.net/phone/member/login"
        # 请求参数
        data = {
            "member_name": "13800002221",
            "password": "q123456"
        }

        # 步骤一：对请求数据进行加密
        diyou = EncryptUtil.get_diyou(data)
        xmdy = EncryptUtil.get_xmdy(diyou)
        print("加密后的请求参数： diyou: {} xmdy:{}".format(diyou, xmdy))

        # 发送请求
        r = self.sesion.post(url=url, data={"diyou":diyou,"xmdy":xmdy})

        # 步骤二：对响应数据diyou解密 提示：解密后的数据为字符串
        r = EncryptUtil.decrypt_data(r.json().get("diyou"))
        print("解密后的diyou为：", r)