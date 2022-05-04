#!/opt/anaconda3/envs python
# coding:utf-8
"""
Name : demo.py
Author  : Martin
Contect : ziqguo@cisco.com
Time    : 2022/5/2 14:43
Desc:
"""
import functools


def decor(sep='-'):
    def wrapper(_func):
        @functools.wraps(_func)
        def inner(*args, **kwargs):
            print(sep*50)
            print('before')
            res = _func(*args, **kwargs)
            print('end')
            print('-' * 50)
            return res
        return inner
    return wrapper


@decor('*')
def func(name, age):
    print(name, age)
    return "func1"


if __name__ == '__main__':
    # new_func = decor(func)
    # new_func()

    res = func('martin', 12)
    print(res)
