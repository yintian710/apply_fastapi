#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 14:40
@file: Register.py
@Desc：
"""
import datetime
from random import randint

from Data.RegisterData import RegisterData
from Data.SendEmailData import SendEmailData
from Error.LoginError.Error import RegisterError
from component.Login import get_password_hash
from component.SendEmail.SendEmail import SendEmail
from tool.Error import GetError, SendEmailError, RedisSetError
from tool.RedisCli import RedisCli
from tool.sql import db
from tool.util import Result, log_for_error


class Register:
    def __init__(self, data: RegisterData):
        self.data = data
        self.username = data.username
        self.password = data.password
        self.nick_name = data.nick_name
        self.email = data.email
        self.db = db
        self.redis = RedisCli()
        self.pwd_hash256 = get_password_hash(self.password)
        self.result = Result()
        self.title = '激活您的账号！'
        self.email_data = {'receiver': self.email, 'title': self.title, 'content': ''}
        self.send = SendEmail(SendEmailData(**self.email_data))

    async def start(self):
        try:
            self.check_all()
            code = self.create_verify_code()
            await self.send_mail(code)
            self.save_2_redis(code)
            self.result.good_result('')
        except (RegisterError, GetError, RedisSetError) as e:
            self.result.bad_result(str(e))
        except Exception as e:
            self.result.bad_result(log_for_error('RegisError!', e))
        return self.result.dict()

    def get_master(self) -> list:
        sql = "select email from `user` where username='yintian'"
        res = self.db.get_one(sql)
        if not res:
            raise GetError('get master email error')
        return res[0]

    def check_all(self):
        sql = f"select username from `user` where username='{self.username}'"
        res = self.db.select(sql)
        if res:
            raise RegisterError('Username repeat !!!')
        sql = f"select username from `user` where email='{self.email}'"
        res = self.db.select(sql)
        if res:
            raise RegisterError('Your email address has been registered！！！')
        sql = f"select username from `user` where nick_name='{self.nick_name}'"
        res = self.db.select(sql)
        if res:
            raise RegisterError('Nick name repeat !!!')

    def regis_2_database(self):
        sql = f"insert into `user` (username, pwd_hash256, nick_name, email, active_time) values ('{self.username}', '{self.pwd_hash256}', '{self.nick_name}', '{self.email}', '{date}')"
        res = self.db.insert_one(sql)
        return res

    async def send_mail(self, code):
        content = f'请点击以下链接激活您的账号！\n\n' \
                  f'http://tool.tintian.icu/active?username={self.username}&code={code}\n\n' \
                  f'此链接十五分钟有效，超时请重新注册'
        self.send.content = content
        await self.send.start()
        if self.send.result.code != 0:
            raise SendEmailError('send email error!')

    def save_2_redis(self, code):
        name = f'{self.username}-active'
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%M')
        sql = f"{code}||insert into `user` (username, pwd_hash256, nick_name, email, active_time) values ('{self.username}', '{self.pwd_hash256}', '{self.nick_name}', '{self.email}', '{date}')"
        self.redis.con.set(name, sql, ex=900)
        if not self.redis.get(name):
            raise RedisSetError('redis set error!')

    @staticmethod
    def create_verify_code():
        code = randint(100000, 999999)
        return code


if __name__ == '__main__':
    data_ = {}
    cls = Register()
