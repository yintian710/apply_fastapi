#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.24 12:07
@file: apply_route.py
@Desc：
"""
from fastapi import APIRouter, Depends

from Data.ApplyInsertData import ApplyInsertData
from Data.ApplyListData import ApplyListData
from Data.GetApplyTimeListData import GetApplyTimeListData
from component.Login.LoginTool import get_current_active_user
from component.apply.ApplyList import ApplyList
from component.apply.GetApplyTimeList import get_apply_time_list
from component.apply.Insert import ApplyInsert

apply = APIRouter(
    prefix='/apply',
    tags=['apply']
)


@apply.post('/insert')
async def _(data: ApplyInsertData, user=Depends(get_current_active_user)):
    cls = ApplyInsert(data, user)
    result = await cls.start()
    return result


@apply.post('/list')
async def _(data: ApplyListData, user=Depends(get_current_active_user)):
    cls = ApplyList(data, user)
    result = await cls.start()
    return result


@apply.post('/getTimeList')
async def _(date: GetApplyTimeListData):
    result = await get_apply_time_list(date)
    return result


if __name__ == '__main__':
    pass
