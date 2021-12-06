#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.12.05 15:52
@file: GetApplyTimeList.py
@Desc：
"""
from tool.util import Result


async def get_apply_time_list(date):
    result = Result()
    return result.good_result(['08:00', '08:30', '09:00', '09:30'])


if __name__ == '__main__':
    pass
