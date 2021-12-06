#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-11-09 9:42
@file: LoginClassData.py
@Desc：
"""
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    wx_open_id: Optional[str] = None
    password: Optional[str] = None

    def set(self, user_id, username, email, wx_open_id, password):
        self.id = user_id
        self.user_name = username
        self.user_email = email
        self.wx_open_id = wx_open_id
        self.password = password


if __name__ == '__main__':
    pass
