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


def decor(_func):
    @functools.wraps(_func)
    def inner():
        print('before')
        _func()
        print('end')
    return inner


@decor
def func():
    print("asdasdasd")


if __name__ == '__main__':
   # new_func = decor(func)
   # new_func()

   func()