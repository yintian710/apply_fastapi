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
    username: str = Field(..., example='_', description='用户名,6-15length', regex='^[a-zA-Z_][\w]{5,14}$')
    password: str = Field(..., example='_', description='6-20length', min_length=6, max_length=20)
    email: str = Field(..., example='_@_.com', description='', regex='^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    nick_name: str = Field('', example='_', description='', min_length=3, max_length=10)


if __name__ == '__main__':
    pass
