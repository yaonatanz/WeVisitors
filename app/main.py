import requests
import re
import math
import random
import time
import uvicorn
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import quote_plus
from http.cookies import SimpleCookie
from datetime import datetime
from fastapi import FastAPI, APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

app = FastAPI()
router = InferringRouter()

@cbv(router)
class Widget:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/add_visitor/", self.add_visitor, methods=["GET"])

    def login(self, username, s):


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=4609753E0DAA3AD80D2A651EEEBCB060B0D04D5DF2E76F9163C8643CA896FD399AA3B8CF8B3E0F44B0D3BEF55094AACF02A63A68313D735BBCA42AC88A15BEA140FE769DF1625229E0287DBF8A43D78F0F3F41BAFC94D54687EEE7B5B19705B56423EB29363B91A4FD65BFAA2665B82EF2F24BAEE854B5EF0447A7AFC11DDAD0',
            'Pragma': 'no-cache',
            'Referer': 'http://5.102.203.91/BackOffice/MainMenu.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        response = s.get('http://5.102.203.91/BackOffice/Default.aspx', headers=headers, verify=False)
        data = self.extract_inputs_from_html(response.text)

        data['txtUserName'] = username
        data['txtPwd'] = '123456'

        encoded_params = '&'.join(f"{quote_plus(str(k), encoding='iso-8859-8')}={quote_plus(str(v), encoding='iso-8859-8')}" for k, v in data.items())


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=4609753E0DAA3AD80D2A651EEEBCB060B0D04D5DF2E76F9163C8643CA896FD399AA3B8CF8B3E0F44B0D3BEF55094AACF02A63A68313D735BBCA42AC88A15BEA140FE769DF1625229E0287DBF8A43D78F0F3F41BAFC94D54687EEE7B5B19705B56423EB29363B91A4FD65BFAA2665B82EF2F24BAEE854B5EF0447A7AFC11DDAD0',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/Default.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        #data = '__VIEWSTATE=%2FwEPDwUKLTQ5ODQxOTQxNA9kFgICBA9kFgICAw8PFgIeBFRleHQFJNeg15nXlNeV15wg16jXm9eR15nXnSAtINeR15LXס;mdefIDE1MGRkZHd79kUvuZJYAFB1INZcY2ExOwnSAtv0sLPQnTEF6JCD&__VIEWSTATEGENERATOR=C3D2AE2E&__EVENTVALIDATION=%2FwEdAAR3wIymefiEJkPhLfjfan%2FuY3plgk0YBAefRz3MyBlTcDPSlu16Yx4QbiDU%2BdddK1Nw4k2%2FCpjT3wswuYEbmowdKTkGlN2z2o5oYnDFjG9Qb68vqAO%2FsV9FuY9iMlFwosc%3D&txtUserName=%E3%E5%F8%E9%FA+%E0%E5%F8%F4%E6&txtPwd=123456&btnOk=%EB%F0%E9%F1%E4'

        response = s.post(
            'http://5.102.203.91/BackOffice/Default.aspx',
            headers=headers,
            data=encoded_params,
            verify=False
        )  
        return response.text

    
    def days_passed_since_2000(self):
        today = datetime.today()
        reference_date = datetime(2000, 1, 1)
        days_passed = (today - reference_date).days      
        return days_passed
    
    def extract_inputs_from_html(self, html_response):
        input_dict = {}
        soup = BeautifulSoup(html_response, 'html.parser')
        input_elements = soup.find_all('input')

        for element in input_elements:
            input_name = element.get('name')
            input_value = element.get('value', '')
            input_dict[input_name] = input_value

        return input_dict

    def add_visitor(self, username: str, duration: int, carNumber: str, hostFirstName:str, hostLastName:str, visitorFirstName:str, visitorLastName:str):
        s = requests.Session()
        status = "OK"
        data = self.login(username, s)

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Connection': 'keep-alive',
            # 'Content-Length': '0',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=25B7FECAB61D9774120BFD449ADB0F467D4CD9357255EE71526C1C9F02332FF532F6F5DAEC92E748E0C493E0401714F994F9C658A5A80704EAF80481E8286E990C6CF5BFEBCCDE802F08BC5B8AF1CF34336010C9659150786E0FDC0C9614A79E3141A752E18550D9DD56392B31D4FC60A5C20B01E6E307014CDC91FAC6661F91',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/MainMenu.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'callback': 'true',
            'param': 'refresh',
        }
        response = s.post(
            'http://5.102.203.91/BackOffice/MainMenu.aspx',
            params=params,
            headers=headers,
            verify=False,
        )

        next_step = {}
        from_login = self.extract_inputs_from_html(data)
        next_step['__EVENTTARGET'] = "btnVisitors"
        next_step['__EVENTARGUMENT'] = ''
        next_step['__VIEWSTATE'] = from_login['__VIEWSTATE']
        next_step['__VIEWSTATEGENERATOR'] = from_login['__VIEWSTATEGENERATOR']
        next_step['__EVENTVALIDATION'] = from_login['__EVENTVALIDATION']
        next_step['txtFreePlaces'] = '1'
        next_step['txtCarQuery'] = ''


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=25B7FECAB61D9774120BFD449ADB0F467D4CD9357255EE71526C1C9F02332FF532F6F5DAEC92E748E0C493E0401714F994F9C658A5A80704EAF80481E8286E990C6CF5BFEBCCDE802F08BC5B8AF1CF34336010C9659150786E0FDC0C9614A79E3141A752E18550D9DD56392B31D4FC60A5C20B01E6E307014CDC91FAC6661F91',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/MainMenu.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        response = s.post('http://5.102.203.91/BackOffice/MainMenu.aspx', headers=headers, data=next_step, verify=False)

        next_step = self.extract_inputs_from_html(response.text)
        next_step.pop('btnBack')

        encoded_params = '&'.join(f"{quote_plus(str(k), encoding='iso-8859-8')}={quote_plus(str(v), encoding='iso-8859-8')}" for k, v in next_step.items())

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=25B7FECAB61D9774120BFD449ADB0F467D4CD9357255EE71526C1C9F02332FF532F6F5DAEC92E748E0C493E0401714F994F9C658A5A80704EAF80481E8286E990C6CF5BFEBCCDE802F08BC5B8AF1CF34336010C9659150786E0FDC0C9614A79E3141A752E18550D9DD56392B31D4FC60A5C20B01E6E307014CDC91FAC6661F91',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/VisitorsList.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        response = s.post(
            'http://5.102.203.91/BackOffice/VisitorsList.aspx',
            headers=headers,
            data=encoded_params,
            verify=False,
        )

        next_step = self.extract_inputs_from_html(response.text)
        ####DURATION
        next_step['__EVENTTARGET'] = 'calToDate'
        next_step['__EVENTARGUMENT'] = str(self.days_passed_since_2000()+duration)
        next_step.pop('btnDel')
        next_step.pop('btnSave')
        next_step.pop('btnCancel')
        next_step.pop('chkPrimaryParking')
        encoded_params = '&'.join(f"{quote_plus(str(k), encoding='iso-8859-8')}={quote_plus(str(v), encoding='iso-8859-8')}" for k, v in next_step.items())

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=25B7FECAB61D9774120BFD449ADB0F467D4CD9357255EE71526C1C9F02332FF532F6F5DAEC92E748E0C493E0401714F994F9C658A5A80704EAF80481E8286E990C6CF5BFEBCCDE802F08BC5B8AF1CF34336010C9659150786E0FDC0C9614A79E3141A752E18550D9DD56392B31D4FC60A5C20B01E6E307014CDC91FAC6661F91',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/Visitors.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        response = s.post('http://5.102.203.91/BackOffice/Visitors.aspx', headers=headers, data=encoded_params, verify=False)


        next_step = self.extract_inputs_from_html(response.text)

        next_step.pop('btnDel')
        next_step.pop('btnCancel')
        next_step.pop('chkPrimaryParking')

        next_step['txtHostFirstName'] = hostFirstName
        next_step['txtHostLastName'] = hostLastName
        next_step['txtVisitorFirstName'] = visitorFirstName
        next_step['txtVisitorLastName'] = visitorLastName
        next_step['txtVisitorCarNumber'] = carNumber

        encoded_params = '&'.join(f"{quote_plus(str(k), encoding='iso-8859-8')}={quote_plus(str(v), encoding='iso-8859-8')}" for k, v in next_step.items())

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=mturbsviswltzknnabfkvt4b; AuthCookie=25B7FECAB61D9774120BFD449ADB0F467D4CD9357255EE71526C1C9F02332FF532F6F5DAEC92E748E0C493E0401714F994F9C658A5A80704EAF80481E8286E990C6CF5BFEBCCDE802F08BC5B8AF1CF34336010C9659150786E0FDC0C9614A79E3141A752E18550D9DD56392B31D4FC60A5C20B01E6E307014CDC91FAC6661F91',
            'Origin': 'http://5.102.203.91',
            'Referer': 'http://5.102.203.91/BackOffice/Visitors.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        response = s.post('http://5.102.203.91/BackOffice/Visitors.aspx', headers=headers, data=encoded_params, verify=False)

        return {"result": status}



widget = Widget()
app.include_router(widget.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)