#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 14:40
@file: Register.py
@Desc：
"""
from random import randint

from Data.RegisterData import RegisterData
from Error.LoginError.Error import RegisterError
from component.Login import get_password_hash
from tool.Error import GetError, RedisSetError
from tool.RedisCli import RedisCli
from tool.sql import db
from tool.util import Result, log_for_error


class Register:
    def __init__(self, data: RegisterData):
        self.data = data
        self.username = data.username
        self.password = data.password
        self.user_email = data.email
        self.wx_open_id = data.wx_open_id
        self.category = data.category
        self.db = db()
        self.redis = RedisCli()
        self.pwd_hash256 = get_password_hash(self.password)
        self.result = Result()

    async def start(self):
        try:
            self.check_all()
            if self.category == -1:
                self.regis_user()
            else:
                self.regis_admin()
            self.result.good_result('注册成功')
        except (RegisterError, GetError, RedisSetError) as e:
            self.result.bad_result(str(e))
        except Exception as e:
            self.result.bad_result(log_for_error('RegisError!', e))
        return self.result

    def check_all(self):
        sql = f"select user_name from `apply_user` where user_name='{self.username}'"
        res = self.db.select(sql)
        if res:
            raise RegisterError('Username repeat !!!')

    def regis_user(self):
        sql = f"insert into `apply_user` (user_name, password, user_email, wx_open_id) values ('{self.username}', '{self.pwd_hash256}', '{self.user_email}', '{self.wx_open_id}')"
        res = self.db.insert_one(sql)
        return res

    def regis_admin(self):
        sql = f"insert into `apply_admin` (user_name, password, user_email, wx_open_id, category) values ('{self.username}', '{self.pwd_hash256}', '{self.user_email}', '{self.wx_open_id}','{self.category}')"
        res = self.db.insert_one(sql)
        return res

    @staticmethod
    def create_verify_code():
        code = randint(100000, 999999)
        return code


if __name__ == '__main__':
    data_ = {}
    # cls = Register()
