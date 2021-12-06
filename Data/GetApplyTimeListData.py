#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.12.05 15:55
@file: GetApplyTimeListData.py
@Desc：
"""
from pydantic import BaseModel


class GetApplyTimeListData(BaseModel):
    date: str = ''


if __name__ == '__main__':
    pass
