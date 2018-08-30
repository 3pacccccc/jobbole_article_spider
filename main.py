# -*- coding:utf-8 -*-
import os
import sys
from scrapy.cmdline import execute

__author__ = 'maruimin'




sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'jobbole'])