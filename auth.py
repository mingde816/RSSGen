# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud

APPID = 'KifmITUG5YwC0N5BkRyGF8RI-gzGzoHsz'
# 填写应用的 APPID

APPKEY = '4ECaPJ9oLpr1UcJ0nBxDuiiw'
# 填写应用的 APPKEY

MASTERKEY = 'hOX3ceh98fNH3D0MUmeFMrPm'
# 填写应用的 MASTERKEY

HEROKUAPP = r'https://mykindle.herokuapp.com/'
# 应用的 heroku 版网址（可不填）

leancloud.init(APPID,APPKEY,master_key=MASTERKEY)
