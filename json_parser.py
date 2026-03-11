#!/usr/bin/env python3
"""json_parser — Recursive descent JSON parser from scratch (no json module). Zero deps."""

class JSONParser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def parse(self):
        self._skip()
        result = self._value()
        self._skip()
        if self.pos < len(self.text):
            raise ValueError(f"Unexpected char at {self.pos}: {self.text[self.pos]}")
        return result

    def _skip(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n\r':
            self.pos += 1

    def _char(self):
        return self.text[self.pos] if self.pos < len(self.text) else None

    def _eat(self, expected):
        if self._char() != expected:
            raise ValueError(f"Expected '{expected}' at {self.pos}, got '{self._char()}'")
        self.pos += 1

    def _value(self):
        self._skip()
        ch = self._char()
        if ch == '"': return self._string()
        if ch == '{': return self._object()
        if ch == '[': return self._array()
        if ch == 't': self._match("true"); return True
        if ch == 'f': self._match("false"); return False
        if ch == 'n': self._match("null"); return None
        if ch in '-0123456789': return self._number()
        raise ValueError(f"Unexpected '{ch}' at {self.pos}")

    def _match(self, word):
        for c in word:
            self._eat(c)

    def _string(self):
        self._eat('"')
        chars = []
        esc = {'n':'\n','t':'\t','r':'\r','\\':'\\','"':'"','/':'/','b':'\b','f':'\f'}
        while self._char() != '"':
            if self._char() == '\\':
                self.pos += 1
                ch = self._char()
                if ch == 'u':
                    self.pos += 1
                    code = self.text[self.pos:self.pos+4]
                    chars.append(chr(int(code, 16)))
                    self.pos += 4
                    continue
                chars.append(esc.get(ch, ch))
            else:
                chars.append(self._char())
            self.pos += 1
        self._eat('"')
        return ''.join(chars)

    def _number(self):
        start = self.pos
        if self._char() == '-': self.pos += 1
        while self._char() and self._char().isdigit(): self.pos += 1
        is_float = False
        if self._char() == '.':
            is_float = True; self.pos += 1
            while self._char() and self._char().isdigit(): self.pos += 1
        if self._char() in 'eE':
            is_float = True; self.pos += 1
            if self._char() in '+-': self.pos += 1
            while self._char() and self._char().isdigit(): self.pos += 1
        s = self.text[start:self.pos]
        return float(s) if is_float else int(s)

    def _array(self):
        self._eat('['); self._skip()
        arr = []
        if self._char() != ']':
            arr.append(self._value())
            self._skip()
            while self._char() == ',':
                self.pos += 1
                arr.append(self._value())
                self._skip()
        self._eat(']')
        return arr

    def _object(self):
        self._eat('{'); self._skip()
        obj = {}
        if self._char() != '}':
            self._skip(); key = self._string(); self._skip()
            self._eat(':'); obj[key] = self._value(); self._skip()
            while self._char() == ',':
                self.pos += 1; self._skip()
                key = self._string(); self._skip()
                self._eat(':'); obj[key] = self._value(); self._skip()
        self._eat('}')
        return obj

def parse_json(text):
    return JSONParser(text).parse()

def main():
    tests = [
        '{"name": "Rogue", "age": 1, "skills": ["Python", "Rust"], "meta": null}',
        '[1, 2.5, -3, 1e10, true, false, null]',
        '{"nested": {"deep": {"value": 42}}, "unicode": "Hello \\u0041"}',
    ]
    for t in tests:
        result = parse_json(t)
        print(f"Input:  {t[:60]}...")
        print(f"Parsed: {result}\n")

if __name__ == "__main__":
    main()
