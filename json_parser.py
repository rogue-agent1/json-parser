#!/usr/bin/env python3
"""json_parser - Recursive descent JSON parser."""
import sys
class JSONParser:
    def __init__(s,text):s.text=text;s.pos=0
    def parse(s):val=s._value();s._ws();return val
    def _ws(s):
        while s.pos<len(s.text) and s.text[s.pos] in " \t\n\r":s.pos+=1
    def _value(s):
        s._ws()
        if s.pos>=len(s.text):raise ValueError("Unexpected EOF")
        c=s.text[s.pos]
        if c=='"':return s._string()
        if c=='{':return s._object()
        if c=='[':return s._array()
        if c in'-0123456789':return s._number()
        if s.text[s.pos:s.pos+4]=="true":s.pos+=4;return True
        if s.text[s.pos:s.pos+5]=="false":s.pos+=5;return False
        if s.text[s.pos:s.pos+4]=="null":s.pos+=4;return None
        raise ValueError(f"Unexpected char: {c}")
    def _string(s):
        s.pos+=1;result=""
        while s.text[s.pos]!='"':
            if s.text[s.pos]=='\\':
                s.pos+=1;esc={"n":"\n","t":"\t","r":"\r","\\":"\\",'"':'"',"/":"/"}.get(s.text[s.pos],s.text[s.pos])
                result+=esc
            else:result+=s.text[s.pos]
            s.pos+=1
        s.pos+=1;return result
    def _number(s):
        start=s.pos
        if s.text[s.pos]=='-':s.pos+=1
        while s.pos<len(s.text) and s.text[s.pos].isdigit():s.pos+=1
        if s.pos<len(s.text) and s.text[s.pos]=='.':
            s.pos+=1
            while s.pos<len(s.text) and s.text[s.pos].isdigit():s.pos+=1
        num=s.text[start:s.pos]
        return float(num) if '.' in num else int(num)
    def _array(s):
        s.pos+=1;s._ws();result=[]
        if s.text[s.pos]==']':s.pos+=1;return result
        result.append(s._value())
        while s._ws() or s.text[s.pos]==',':s.pos+=1;result.append(s._value())
        s.pos+=1;return result
    def _object(s):
        s.pos+=1;s._ws();result={}
        if s.text[s.pos]=='}':s.pos+=1;return result
        key=s._string();s._ws();s.pos+=1;result[key]=s._value()
        while s._ws() or s.text[s.pos]==',':s.pos+=1;s._ws();key=s._string();s._ws();s.pos+=1;result[key]=s._value()
        s._ws();s.pos+=1;return result
if __name__=="__main__":
    tests=['{"name":"Alice","age":30,"scores":[95,87,92]}','[1,2,3,true,null,"hello"]','{"nested":{"a":{"b":1}}}']
    for t in tests:
        result=JSONParser(t).parse();print(f"  {t[:50]:50s} => {result}")
