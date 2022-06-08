import base64
import sys
import time
import execjs
import arrow
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from jshmac import get_sha256
import requests
from requests.cookies import RequestsCookieJar
import value
from fake_useragent import UserAgent


class HuaWei:
    def __init__(self, text, j_time):
        self.session = requests.Session()
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'referer': 'https://ppstore.jd.com/'
        }
        self.session.headers.update(headers)

        tmp_cookies = RequestsCookieJar()

        for item in value.selenium_cookies:
            tmp_cookies.set(item["name"], item["value"])
        self.session.cookies.update(tmp_cookies)

        self.api_url = 'https://pp-api.jd.com/api'

        self.text_7 = text
        self.j_time = j_time
        self.commodity_id = [
            {'name': '40e5', 'id': 3609},
            {'name': '405', 'id': 3516},
            {'name': 'x2', 'id': 3648},
            {'name': 'rs', 'id': 3382},
            {'name': '40p+', 'id': 3381},
            {'name': '40p', 'id': 3368},
        ]

    def rest(self):
        time.sleep(self.j_time)

    def read_js(self, word):
        with open('hmac.js') as f:
            jsText = f.read()
        js = execjs.compile(jsText)
        sign = js.call('HmacSHA256_Encrypt', word)
        return sign

    def get_list(self, modelId, page=1):
        timestamp = str(int(time.time() * 1000))
        word = 'retail.store.product.query&paipai-selected-retail-store&{"pageNo":%d,"pageSize":500,"brand":{"key":8557,"label":"华为（HUAWEI）"},"modelId":%d,"quality":[99,95],"brandId":8557,"createAtStart":null,"createAtEnd":null,"cat3":655,"X-Paipai-Api-Gateway-OrgId":59}&pc&%s' % (page, modelId, timestamp)
        sign = get_sha256(word)
        params = {
            'apiName': 'retail.store.product.query',
            'appKey': 'paipai-selected-retail-store',
            'timestamp': timestamp,
            'loginType': 'pc',
            'sign': sign,
            'body': '{"pageNo":%d,"pageSize":500,"brand":{"key":8557,"label":"华为（HUAWEI）"},"modelId":%d,"quality":[99,95],"brandId":8557,"createAtStart":null,"createAtEnd":null,"cat3":655,"X-Paipai-Api-Gateway-OrgId":59}' % (page, modelId)
        }
        resp = self.session.get(self.api_url, params=params)
        if resp.json()['msg']:
            msg = resp.json()['msg']
            self.text_7.append(msg)
        phone_list = resp.json()['data']['list']
        totalPages = resp.json()['data']['totalPages']
        totalElements = resp.json()['data']['totalElements']

        return phone_list, totalPages, totalElements

    def screen(self, phone_list, noNum_list):
        today = arrow.now()
        today_6 = str(today.shift(months=-6))[:10]
        today_6_mk = time.mktime(time.strptime(today_6, '%Y-%m-%d'))
        for phone in phone_list:
            inStockAge = phone['inStockAge']
            if '0.04' in inStockAge:
                attrValueName = phone['inspectReportAttrValues'][0]['attrValueName'][:10]
                if len(attrValueName) > 7:
                    attrValue = time.mktime(time.strptime(attrValueName, '%Y-%m-%d'))
                    if attrValue > today_6_mk:
                        itemGoodsNo = phone['itemGoodsNo']
                        if itemGoodsNo not in noNum_list:
                            uniqueCode = phone['uniqueCode']
                            noNum_list.append(itemGoodsNo)
                            self.get_img(itemGoodsNo, attrValueName, uniqueCode)

    def get_img(self, itemGoodsNo, attrValueName, uniqueCode):
        timestamp = str(int(time.time() * 1000))
        word = 'retail.store.product.code.online.print&paipai-selected-retail-store&{"itemGoodsNo":%s,"salesPlatform":2,"storeId":"8","X-Paipai-Api-Gateway-OrgId":59}&pc&%s' % (itemGoodsNo, timestamp)
        sign = get_sha256(word)
        params = {
            'apiName': 'retail.store.product.code.online.print',
            'appKey': 'paipai-selected-retail-store',
            'timestamp': timestamp,
            'loginType': 'pc',
            'sign': sign,
            'body': '{"itemGoodsNo":%s,"salesPlatform":2,"storeId":"8","X-Paipai-Api-Gateway-OrgId":59}' % (itemGoodsNo)
        }
        resp = self.session.get(self.api_url, params=params)
        channelItemSkuName = resp.json()['data']['channelItemSkuName']
        codeInfo = resp.json()['data']['codeInfo']
        qualityName = resp.json()['data']['qualityName']
        data = base64.b64decode(codeInfo)
        with open(f'C:/图片/{channelItemSkuName}-{qualityName}-{attrValueName}-{itemGoodsNo}-{uniqueCode}.png', 'wb') as f:
            f.write(data)

    def crawl(self, modelId):
        noNum_list = []
        old_num = 0
        count = 1
        while True:
            try:
                self.text_7.append(f'第{count}次爬取！')
                phone_list, totalPages, totalElements = self.get_list(modelId)
                if totalElements != old_num:
                    old_num = totalElements
                    if totalPages != 1:
                        phone_list_1, totalPages, totalElements = self.get_list(modelId, page=2)
                        phone_list = phone_list_1 + phone_list
                    self.screen(phone_list, noNum_list)
                self.rest()
                count += 1
         
            except:
                self.text_7.append('休息一下')
                time.sleep(60)

            # phone_list_flag = self.get_list(modelId)
            # phone_list = phone_list_flag[0]
            # if phone_list_flag:
            #     if phone_list_flag[2] != old_num:
            #         old_num = phone_list_flag[2]
            #         if phone_list_flag[1] != 1:
            #             phone_list_flag = self.get_list(modelId, page=2)
            #             phone_list = phone_list_flag[0]

    def test(self, modelId):
        while True:
            resp = requests.get('https://me.bfsea.xyz/')
            self.text_7.append(str(resp.status_code))
            self.rest()

    def run(self):
        pool = ThreadPoolExecutor(6)
        ts = []
        for commodity in self.commodity_id:
            ts.append(pool.submit(self.crawl, commodity['id']))
            # ts.append(pool.submit(self.test, commodity['id']))
        for future in as_completed(ts):
            data = future.result()
            # print("in main: get page {}s success".format(data))
