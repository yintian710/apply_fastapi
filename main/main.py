#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.03 09:30
@file: main.py
@Desc：
"""
import os
import sys

import uvicorn
from fastapi import FastAPI

from component.Login.LoginTool import merry_login

path = os.getcwd()
work_path = path.split('/main')[0]
sys.path.append(work_path)
sys.path.append(work_path + '/main')
from routes.login_route import login
from routes.apply_route import apply

app = FastAPI(docs_url='/yintian', redoc_url='/re_yintian')

route_list = [
    login,
    apply
]

for route in route_list:
    app.include_router(route)


@app.get('/h')
async def h():
    return 'Hello World'


if __name__ == '__main__':
    print(merry_login.logger.disabled)
    uvicorn.run(app='main:app', host='0.0.0.0', port=7100)
