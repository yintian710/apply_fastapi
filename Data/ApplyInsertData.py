#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.22 20:35
@file: ApplyInsertData.py
@Desc：
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class Times(BaseModel):
    start: datetime
    end: datetime


class ApplyInsertData(BaseModel):
    organization: str
    user_name: str
    profession_class: str
    address: int = 0
    apply_type: int = 0
    need_stereo: int = 0
    times: List[Times]
    checked: int = 0
    remark: str = ''
    admin_id: int = 1
    user_id: int = 1
    content: str
    app_id: int = -1


if __name__ == '__main__':
    pass
