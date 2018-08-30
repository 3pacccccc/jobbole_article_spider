# -*- coding:utf-8 -*-
__author__ = 'maruimin'

from hashlib import md5




# def get_md5(value):
#     if isinstance(value, str):
#         value = value.encode('utf-8')
#     m = md5()
#     m.update(value)
#     return m.hexdigest()

def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')

    m = md5()
    m.update(text)
    return m.hexdigest()



if __name__ == '__main__':
    print(get_md5('http://blog.jobbole.com/114276'))
