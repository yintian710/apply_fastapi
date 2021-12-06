#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.22 17:42
@file: Insert.py
@Desc：
"""
from Data.ApplyInsertData import ApplyInsertData
from Data.LoginClassData import User
from Error.ApplyError.Error import TimeError
from tool.sql import db
from tool.util import Result


class ApplyInsert:
    def __init__(self, data: ApplyInsertData, user: User):
        self.data = data
        self.db = db()
        self.user = user
        self.result = Result()

    async def start(self):
        try:
            await self.check_all()
            await self.insert_all()
        except TimeError as e:
            return self.result.bad_result(str(e))
        except Exception as e:
            return self.result.error(e)
        return self.result.good_result('操作成功')

    async def check_all(self):
        for _ in self.data.times:
            res = self.db.select(f"select id from apply_application where start_time between '{_.start.strftime('%Y-%m-%d %H:%M:%S')}' and '{_.end.strftime('%Y-%m-%d %H:%M:%S')}' or  end_time between '{_.start.strftime('%Y-%m-%d %H:%M:%S')}' and '{_.end.strftime('%Y-%m-%d %H:%M:%S')}'")
            if res:
                raise TimeError(f"{_.start.strftime('%Y-%m-%d %H:%M:%S')} 与 {_.end.strftime('%Y-%m-%d %H:%M:%S')} 时间段已被申请")
            if (_.end - _.start).total_seconds() < 3600:
                raise TimeError('最少活动间隔时间为 1 小时')
        max_app_id = self.db.get_one('select max(app_id) from apply_application')[0]
        self.data.app_id = max_app_id + 1
        self.data.user_id = self.user.id

    async def insert_all(self):
        for _ in self.data.times:
            self.db.insert_one(f"insert into apply_application(organization, user_name, profession_class, address, " \
                               f"apply_type, need_stereo, start_time, end_time, checked, remark, admin_id, user_id, app_id, content)" \
                               f" values ('{self.data.organization}','{self.data.user_name}','{self.data.profession_class}'" \
                               f",'{self.data.address}','{self.data.apply_type}','{self.data.need_stereo}','{_.start}'," \
                               f"'{_.end}','{self.data.checked}','{self.data.remark}','{self.data.admin_id}','{self.data.user_id}','{self.data.app_id}', '{self.data.content}')")


if __name__ == '__main__':
    pass
