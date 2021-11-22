#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-11-09 9:25
@file: login_route.py
@Desc：
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from Data.LoginClassData import User, Token
from Data.RegisterData import RegisterData
from component.Login.LoginCONTENT import fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from component.Login.LoginTool import authenticate_user, create_access_token, get_current_active_user, \
    verify_for_regis_, activate_account
from component.Login.Register import Register

login = APIRouter(
    prefix='/login',
    tags=['login']
)


@login.post('', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@login.post('/regis')
async def regis(data: RegisterData):
    cls = Register(data)
    result = await cls.start()
    return result


@login.get('/activate')
async def activate(code: str, username: str):
    result = activate_account(code, username)
    return result


@login.get('/verify')
async def verify_for_regis(username: str, code: str):
    result = verify_for_regis_(username, code)
    return result


@login.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@login.get("/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


if __name__ == '__main__':
    pass
