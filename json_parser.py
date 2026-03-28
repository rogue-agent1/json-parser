#!/usr/bin/env python3
"""Pure Python JSON parser (no json module)."""
import sys
class JsonParser:
    def __init__(self,text): self.text=text; self.pos=0
    def parse(self):
        self._ws(); v=self._value(); self._ws(); return v
    def _ws(self):
        while self.pos<len(self.text) and self.text[self.pos] in " \t\n\r": self.pos+=1
    def _value(self):
        c=self.text[self.pos]
        if c=='"': return self._string()
        if c=='{': return self._object()
        if c=='[': return self._array()
        if c in '-0123456789': return self._number()
        if self.text[self.pos:self.pos+4]=='true': self.pos+=4; return True
        if self.text[self.pos:self.pos+5]=='false': self.pos+=5; return False
        if self.text[self.pos:self.pos+4]=='null': self.pos+=4; return None
        raise ValueError(f"Unexpected char at {self.pos}: {c}")
    def _string(self):
        self.pos+=1; s=""
        while self.text[self.pos]!='"':
            if self.text[self.pos]=='\\':
                self.pos+=1; c=self.text[self.pos]
                esc={'n':'\n','t':'\t','r':'\r','"':'"','\\':'\\','/':'/'}
                if c in esc: s+=esc[c]
                elif c=='u': s+=chr(int(self.text[self.pos+1:self.pos+5],16)); self.pos+=4
            else: s+=self.text[self.pos]
            self.pos+=1
        self.pos+=1; return s
    def _number(self):
        start=self.pos
        if self.text[self.pos]=='-': self.pos+=1
        while self.pos<len(self.text) and self.text[self.pos].isdigit(): self.pos+=1
        if self.pos<len(self.text) and self.text[self.pos]=='.':
            self.pos+=1
            while self.pos<len(self.text) and self.text[self.pos].isdigit(): self.pos+=1
            return float(self.text[start:self.pos])
        if self.pos<len(self.text) and self.text[self.pos] in 'eE':
            self.pos+=1
            if self.text[self.pos] in '+-': self.pos+=1
            while self.pos<len(self.text) and self.text[self.pos].isdigit(): self.pos+=1
            return float(self.text[start:self.pos])
        return int(self.text[start:self.pos])
    def _array(self):
        self.pos+=1; self._ws(); arr=[]
        if self.text[self.pos]==']': self.pos+=1; return arr
        arr.append(self._value()); self._ws()
        while self.text[self.pos]==',': self.pos+=1; self._ws(); arr.append(self._value()); self._ws()
        self.pos+=1; return arr
    def _object(self):
        self.pos+=1; self._ws(); obj={}
        if self.text[self.pos]=='}': self.pos+=1; return obj
        k=self._string(); self._ws(); self.pos+=1; self._ws(); obj[k]=self._value(); self._ws()
        while self.text[self.pos]==',': self.pos+=1; self._ws(); k=self._string(); self._ws(); self.pos+=1; self._ws(); obj[k]=self._value(); self._ws()
        self.pos+=1; return obj
if __name__=="__main__":
    import json
    tests=['42','"hello"','true','null','[1,2,3]','{"a":1,"b":"c"}','{"nested":{"x":[1,2.5,null,true]}}']
    for t in tests:
        mine=JsonParser(t).parse(); ref=json.loads(t)
        assert mine==ref,f"FAIL: {t}"
    print("All JSON parser tests passed")
