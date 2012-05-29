#! /usr/bin/python
import new
def funct(a):
    strfunc = "\
def foo(): \
x = "+str(a)+"; return type(x)"
    co = compile ( strfunc, '', 'exec' )
    
    ns = {}
    exec co in ns
    nfunc = new.function(ns["foo"].func_code, globals(), 'foo' )
    globals()['foo'] = nfunc



funct(list())
print globals()['list']()
