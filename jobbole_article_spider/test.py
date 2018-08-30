# -*- coding:utf-8 -*-
__author__ = 'maruimin'
import re
import requests


if __name__ == '__main__':
   response = requests.get('http://www.dygang.net/')
   print(response.text)