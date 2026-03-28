#!/usr/bin/env python3
"""JSON parser from scratch (no json module)."""
import sys
def parse(s,i=0):
    i=skip(s,i)
    if s[i]=='"': return parse_string(s,i)
    if s[i]=='{': return parse_object(s,i)
    if s[i]=='[': return parse_array(s,i)
    if s[i] in '-0123456789': return parse_number(s,i)
    if s[i:i+4]=='true': return True,i+4
    if s[i:i+5]=='false': return False,i+5
    if s[i:i+4]=='null': return None,i+4
    raise ValueError(f"Unexpected char at {i}: {s[i]}")
def skip(s,i):
    while i<len(s) and s[i] in ' \t\n\r': i+=1
    return i
def parse_string(s,i):
    i+=1;start=i;result=[]
    while s[i]!='"':
        if s[i]=='\\':
            i+=1;esc={'n':'\n','t':'\t','r':'\r','\\':'\\','"':'"','/':'/'}
            if s[i] in esc: result.append(esc[s[i]])
            elif s[i]=='u': result.append(chr(int(s[i+1:i+5],16)));i+=4
            i+=1
        else: result.append(s[i]);i+=1
    return ''.join(result),i+1
def parse_number(s,i):
    start=i
    if s[i]=='-': i+=1
    while i<len(s) and s[i].isdigit(): i+=1
    if i<len(s) and s[i]=='.':
        i+=1
        while i<len(s) and s[i].isdigit(): i+=1
    if i<len(s) and s[i] in 'eE':
        i+=1
        if i<len(s) and s[i] in '+-': i+=1
        while i<len(s) and s[i].isdigit(): i+=1
    num=s[start:i]
    return (float(num) if '.' in num or 'e' in num or 'E' in num else int(num)),i
def parse_array(s,i):
    i=skip(s,i+1);arr=[]
    if s[i]==']': return arr,i+1
    while True:
        val,i=parse(s,i);arr.append(val);i=skip(s,i)
        if s[i]==']': return arr,i+1
        i=skip(s,i+1)
def parse_object(s,i):
    i=skip(s,i+1);obj={}
    if s[i]=='}': return obj,i+1
    while True:
        i=skip(s,i);key,i=parse_string(s,i);i=skip(s,i)
        i=skip(s,i+1);val,i=parse(s,i);obj[key]=val;i=skip(s,i)
        if s[i]=='}': return obj,i+1
        i=skip(s,i+1)
def main():
    if "--demo" in sys.argv:
        tests=['{"name":"Alice","age":30,"scores":[95,87.5],"active":true,"addr":null}',
               '[1, 2, [3, 4], {"a": "b"}]','42','"hello\\nworld"']
        for t in tests:
            result,_=parse(t);print(f"{t[:50]}... → {result}")
    else:
        data=sys.stdin.read();result,_=parse(data);print(result)
if __name__=="__main__": main()
