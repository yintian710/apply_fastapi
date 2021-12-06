#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.24 15:54
@file: ApplyListData.py
@Desc：
"""
from typing import Optional

from pydantic import BaseModel

from Data.ApplyInsertData import Times


class ApplyListData(BaseModel):
    times: Optional[Times] = None
    organization: Optional[str] = None
    user_name: Optional[str] = None
    address: int = -1
    apply_type: int = -1
    need_stereo: int = -1
    checked: int = -1
    admin_id: int = -1
    user_id: int = -1


if __name__ == '__main__':
    pass
