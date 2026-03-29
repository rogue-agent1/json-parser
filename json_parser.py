#!/usr/bin/env python3
"""JSON parser from scratch. Zero dependencies."""

class JSONParser:
    def __init__(self, text):
        self.text = text; self.pos = 0

    def parse(self):
        self._skip_ws()
        result = self._value()
        self._skip_ws()
        if self.pos < len(self.text): raise ValueError(f"Unexpected char at {self.pos}")
        return result

    def _skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos] in " \t\n\r": self.pos += 1

    def _value(self):
        self._skip_ws()
        if self.pos >= len(self.text): raise ValueError("Unexpected end")
        ch = self.text[self.pos]
        if ch == '"': return self._string()
        if ch == '{': return self._object()
        if ch == '[': return self._array()
        if ch == 't': return self._literal("true", True)
        if ch == 'f': return self._literal("false", False)
        if ch == 'n': return self._literal("null", None)
        if ch in '-0123456789': return self._number()
        raise ValueError(f"Unexpected '{ch}' at {self.pos}")

    def _string(self):
        self.pos += 1; result = []
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch == '"': self.pos += 1; return "".join(result)
            if ch == '\\':
                self.pos += 1; esc = self.text[self.pos]
                result.append({'n':'\n','t':'\t','r':'\r','"':'"','\\':'\\','/':'/'}.get(esc, esc))
            else: result.append(ch)
            self.pos += 1
        raise ValueError("Unterminated string")

    def _number(self):
        start = self.pos
        if self.text[self.pos] == '-': self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        if self.pos < len(self.text) and self.text[self.pos] in 'eE':
            self.pos += 1
            if self.pos < len(self.text) and self.text[self.pos] in '+-': self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        s = self.text[start:self.pos]
        return float(s) if '.' in s or 'e' in s or 'E' in s else int(s)

    def _object(self):
        self.pos += 1; obj = {}
        self._skip_ws()
        if self.text[self.pos] == '}': self.pos += 1; return obj
        while True:
            self._skip_ws(); key = self._string()
            self._skip_ws(); assert self.text[self.pos] == ':'; self.pos += 1
            obj[key] = self._value()
            self._skip_ws()
            if self.text[self.pos] == '}': self.pos += 1; return obj
            assert self.text[self.pos] == ','; self.pos += 1

    def _array(self):
        self.pos += 1; arr = []
        self._skip_ws()
        if self.text[self.pos] == ']': self.pos += 1; return arr
        while True:
            arr.append(self._value())
            self._skip_ws()
            if self.text[self.pos] == ']': self.pos += 1; return arr
            assert self.text[self.pos] == ','; self.pos += 1

    def _literal(self, word, value):
        if self.text[self.pos:self.pos+len(word)] == word:
            self.pos += len(word); return value
        raise ValueError(f"Expected {word} at {self.pos}")

def parse_json(text): return JSONParser(text).parse()

if __name__ == "__main__":
    import sys
    print(parse_json(sys.stdin.read() if not sys.argv[1:] else sys.argv[1]))
