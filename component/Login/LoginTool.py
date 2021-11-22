#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-11-09 9:45
@file: LoginTool.py
@Desc：
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from Data.LoginClassData import UserInDB, TokenData, User
from component.Login.LoginCONTENT import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme, fake_users_db
from setting.content import not_auth_exception, find_user_exception
from tool.RedisCli import RedisCli
from tool.sql import db
from tool.util import Result, MerryTool


merry_login = MerryTool()
merry_login.logger.disabled = 1


# @merry.merry_except(Exception)
# def process_


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_for_regis_(username: str, code: str):
    pass


def activate_account(code: str, username: str):
    redis = RedisCli()
    result = Result()
    name = f'{username}-active'
    res = redis.get(name)
    if not res:
        return result.bad_result('no this account to activate!')
    code_, sql = res.split('||')
    if code_ != code:
        return result.bad_result('激活失败！账号激活码不正确！')
    user_id = db.insert_one(sql)
    if not user_id:
        return result.bad_result('激活失败！清重试！')
    redis.con.delete(name)
    return result.good_result(f'用户{username}激活成功！')
    #     if not res:
    #         return result.bad_result('activate error for update')
    #     return result.good_result('activate successful!')
    # else:
    #     return result.bad_result(f'inspect your account code: {res[0]}!')


@merry_login.merry_try
def get_user(username: str) -> User:
    sql = f"select user_id, username, pwd_hash256, email, nick_name, status, permissions from user where username='{username}'"
    user_res = db.get_one(sql)
    if not user_res:
        raise find_user_exception
    user = User()
    sql = f"select a.role from authorization a left join user u on a.user_id=u.user_id where u.username='{username}'"
    rule_res = db.select(sql)
    rule = ['user']
    if rule_res:
        for _ in rule_res:
            rule += _
    user.set(*user_res, rule)
    return user


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.pwd_hash256):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise not_auth_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise not_auth_exception
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = await verify(token)
    user = get_user(username=token_data.username)
    if user is None:
        raise not_auth_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.status != 0:
        raise HTTPException(status_code=400, detail=f"Inactive user - {current_user.status}")
    return current_user


if __name__ == '__main__':
    a = get_password_hash('yintian')
    print(a)
