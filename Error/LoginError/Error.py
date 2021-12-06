#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 15:21
@file: Error.py
@Desc：
"""


class RegisterError(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    pass
