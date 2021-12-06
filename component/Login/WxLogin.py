#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.12.06 14:47
@file: WxLogin.py
@Desc：
"""
import base64
import json

from Crypto.Cipher import AES

from Data.WxLoginData import WxLoginData
from tool.async_base_httpx import AsyncBaseHttpx


class WxLogin(AsyncBaseHttpx):
    def __init__(self, data: WxLoginData, task='WxLogin'):
        super().__init__(task)
        self.code = data.code
        self.open_id = data.open_id
        self.session_key = ''
        self.secret = '9acbe6e9daf96b53150f871d12b8f5e5'
        self.app_id = 'wxf0adf8708a4d89cd'
        self.openid = ''
        self.encrypted_data = data.encrypted_data
        self.iv = data.iv
        self.user_info = data.user_info

    async def start(self):
        res = await self.wx_login()
        self.decrypt()

    async def wx_login(self):
        url = f'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': self.app_id,
            'secret': self.secret,
            'js_code': self.code,
            'grant_type': 'authorization_code'
        }
        res = await self.session.get(url, params=params)
        res_text = res.text
        if res.status_code == 200:
            self.session_key = json.loads(res_text)['session_key']
            self.openid = json.loads(res_text)['openid']
        self.call_print(res)

    def decrypt(self, ):
        # base64 decode
        session_key = base64.b64decode(self.session_key)
        encrypted_data = base64.b64decode(self.encrypted_data)
        iv = base64.b64decode(self.iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)))

        if decrypted['watermark']['appid'] != self.app_id:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == '__main__':
    pass
