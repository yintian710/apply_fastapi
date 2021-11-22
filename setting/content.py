#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-11-09 10:31
@file: content.py
@Desc：
"""
from fastapi import HTTPException
from starlette import status

not_auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

find_user_exception = HTTPException(
    status_code=status.HTTP_502_BAD_GATEWAY,
    detail="Find user error",
    headers={"WWW-Authenticate": "Bearer"},
)

if __name__ == '__main__':
    pass
