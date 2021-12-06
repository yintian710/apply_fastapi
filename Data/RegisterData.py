#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 14:42
@file: RegisterData.py
@Desc：
"""
from pydantic import BaseModel, Field


class RegisterData(BaseModel):
    username: str = Field(..., example='_', description='用户名,5-15length', regex='^[a-zA-Z_][\w]{4,14}$')
    password: str = Field(..., example='_', description='用户密码,6-20长度', min_length=6, max_length=20)
    email: str = Field('_@_.com', example='_@_.com', description='用户邮箱',
                       regex='^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    wx_open_id: str = Field('', description='用户微信openid')
    category: int = Field(-1, description='用户权限')


if __name__ == '__main__':
    pass
