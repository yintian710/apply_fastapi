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
    username: Optional[str] = None
    email: Optional[str] = None
    nick_name: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[str] = None
    pwd_hash256: Optional[str] = None
    authorization: Optional[str] = None
    permissions: Optional[str] = None

    def set(self, user_id, username, pwd_hash256, email, nick_name, status, permissions, authorization):
        self.user_id = user_id
        self.username = username
        self.pwd_hash256 = pwd_hash256
        self.email = email
        self.nick_name = nick_name
        self.status = status
        self.permissions = permissions
        self.authorization = authorization


if __name__ == '__main__':
    pass
