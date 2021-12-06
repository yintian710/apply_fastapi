#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.12.06 14:50
@file: WxLoginData.py
@Desc：
"""
from pydantic import BaseModel

# class WxLoginInfo(BaseModel):


class WxLoginData(BaseModel):
    code: str
    open_id: str = ''
    encrypted_data: str = ''
    iv: str = ''
    user_info: str = ''


if __name__ == '__main__':
    pass
