#!/usr/bin/env python3
"""JSON parser from scratch (no json module)."""
import sys
def parse(s,i=0):
    i=skip(s,i)
    if s[i]=='"': return parse_str(s,i)
    if s[i] in '-0123456789': return parse_num(s,i)
    if s[i]=='{': return parse_obj(s,i)
    if s[i]=='[': return parse_arr(s,i)
    if s[i:i+4]=='true': return True,i+4
    if s[i:i+5]=='false': return False,i+5
    if s[i:i+4]=='null': return None,i+4
    raise ValueError(f"Unexpected char at {i}: {s[i]}")
def skip(s,i):
    while i<len(s) and s[i] in ' \t\n\r': i+=1
    return i
def parse_str(s,i):
    i+=1; start=i
    while s[i]!='"':
        if s[i]=='\\': i+=2
        else: i+=1
    return s[start:i].replace('\\n','\n').replace('\\t','\t').replace('\\"','"').replace('\\\\','\\'),i+1
def parse_num(s,i):
    start=i
    if s[i]=='-': i+=1
    while i<len(s) and s[i].isdigit(): i+=1
    if i<len(s) and s[i]=='.':
        i+=1
        while i<len(s) and s[i].isdigit(): i+=1
    n=s[start:i]
    return (float(n) if '.' in n else int(n)),i
def parse_obj(s,i):
    i=skip(s,i+1); obj={}
    if s[i]=='}': return obj,i+1
    while True:
        key,i=parse_str(s,skip(s,i)); i=skip(s,i)+1  # skip :
        val,i=parse(s,i); obj[key]=val; i=skip(s,i)
        if s[i]=='}': return obj,i+1
        i+=1  # skip ,
def parse_arr(s,i):
    i=skip(s,i+1); arr=[]
    if s[i]==']': return arr,i+1
    while True:
        val,i=parse(s,i); arr.append(val); i=skip(s,i)
        if s[i]==']': return arr,i+1
        i+=1
text=sys.stdin.read() if len(sys.argv)<2 else (open(sys.argv[1]).read() if '.' in sys.argv[1] else sys.argv[1])
result,_=parse(text)
import json; print(json.dumps(result,indent=2))
