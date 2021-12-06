#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.24 15:52
@file: ApplyList.py
@Desc：
"""
from Data.ApplyListData import ApplyListData
from Data.LoginClassData import User
from Error.ApplyError.Error import TimeError
from tool.sql import db
from tool.util import Result


class ApplyList:
    def __init__(self, data: ApplyListData, user: User):
        self.data = data
        self.result = Result()
        self.user = user
        self.db = db()

    async def start(self):
        try:
            result = await self.get_list()
        except Exception as e:
            return self.result.error(e)
        return result

    async def get_where(self):
        sql_where = ' where '
        if self.data.times:
            if self.data.times.start > self.data.times.end:
                raise TimeError('查询开始时间要小于结束时间')
            sql_where += f"start_time between '{self.data.times.start.strftime('%Y-%m-%d %H:%M:%S')}' and '{self.data.times.end.strftime('%Y-%m-%d %H:%M:%S')}' or  end_time between '{self.data.times.start.strftime('%Y-%m-%d %H:%M:%S')}' and '{self.data.times.end.strftime('%Y-%m-%d %H:%M:%S')}'"
        if self.data.user_name:
            sql_where += f' and user_name={self.data.user_name}'
        if self.data.organization:
            sql_where += f' and organization={self.data.organization}'
        if self.data.address != -1:
            sql_where += f' and address={self.data.address}'
        if self.data.apply_type != -1:
            sql_where += f' and apply_type={self.data.apply_type}'
        if self.data.need_stereo != -1:
            sql_where += f' and need_stereo={self.data.need_stereo}'
        if self.data.checked != -1:
            sql_where += f' and checked={self.data.checked}'
        if self.data.admin_id != -1:
            sql_where += f' and admin_id={self.data.admin_id}'
        if self.data.user_id != -1:
            sql_where += f' and user_id={self.data.user_id}'
        if sql_where == ' where ':
            return ''
        return sql_where

    async def get_list(self):
        sql = f'select organization, user_name, profession_class, address, apply_type, need_stereo, start_time, end_time, checked, remark, admin_id, user_id, content, app_id from apply_application'
        sql += await self.get_where()
        res = self.db.select(sql)
        self.result.list = list(res)
        return self.result.good_result('获取成功')


if __name__ == '__main__':
    pass
