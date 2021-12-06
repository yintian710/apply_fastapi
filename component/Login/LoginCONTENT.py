#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-11-09 9:38
@file: LoginCONTENT.py
@Desc：
"""
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "yintian710"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

fake_users_db = {
    "yintian": {
        "username": "yintian",
        "full_name": "yintian",
        "email": "yintian710@gmail.com",
        "hashed_password": "$2b$12$kJNnWDNBOncH4hDC.TD6KuUYL/AJOEdCnhQwCBV6CqZ4LFp9saa5C",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

if __name__ == '__main__':
    pass
