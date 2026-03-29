#!/usr/bin/env python3
"""JSON parser from scratch — no json module. Includes formatter and validator."""
import sys

class JSONError(Exception): pass

class Parser:
    def __init__(self, text):
        self.text = text; self.pos = 0

    def skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos] in " \t\n\r": self.pos += 1

    def peek(self):
        self.skip_ws()
        return self.text[self.pos] if self.pos < len(self.text) else None

    def consume(self, expected=None):
        self.skip_ws()
        if self.pos >= len(self.text): raise JSONError("Unexpected EOF")
        c = self.text[self.pos]
        if expected and c != expected: raise JSONError(f"Expected '{expected}' got '{c}' at {self.pos}")
        self.pos += 1; return c

    def parse(self):
        self.skip_ws()
        result = self.value()
        self.skip_ws()
        if self.pos < len(self.text): raise JSONError(f"Trailing content at {self.pos}")
        return result

    def value(self):
        c = self.peek()
        if c == '"': return self.string()
        if c == '{': return self.object()
        if c == '[': return self.array()
        if c == 't': return self.literal("true", True)
        if c == 'f': return self.literal("false", False)
        if c == 'n': return self.literal("null", None)
        if c in '-0123456789': return self.number()
        raise JSONError(f"Unexpected '{c}' at {self.pos}")

    def string(self):
        self.consume('"'); chars = []
        while self.pos < len(self.text):
            c = self.text[self.pos]; self.pos += 1
            if c == '"': return "".join(chars)
            if c == '\\':
                esc = self.text[self.pos]; self.pos += 1
                if esc == 'n': chars.append('\n')
                elif esc == 't': chars.append('\t')
                elif esc == 'r': chars.append('\r')
                elif esc == '\\': chars.append('\\')
                elif esc == '"': chars.append('"')
                elif esc == '/': chars.append('/')
                elif esc == 'u':
                    h = self.text[self.pos:self.pos+4]; self.pos += 4
                    chars.append(chr(int(h, 16)))
                else: chars.append(esc)
            else: chars.append(c)
        raise JSONError("Unterminated string")

    def number(self):
        start = self.pos
        if self.text[self.pos] == '-': self.pos += 1
        while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        is_float = False
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            is_float = True; self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        if self.pos < len(self.text) and self.text[self.pos] in 'eE':
            is_float = True; self.pos += 1
            if self.pos < len(self.text) and self.text[self.pos] in '+-': self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        s = self.text[start:self.pos]
        return float(s) if is_float else int(s)

    def object(self):
        self.consume('{'); result = {}
        if self.peek() == '}': self.consume('}'); return result
        while True:
            key = self.string()
            self.consume(':')
            result[key] = self.value()
            if self.peek() == '}': self.consume('}'); return result
            self.consume(',')

    def array(self):
        self.consume('['); result = []
        if self.peek() == ']': self.consume(']'); return result
        while True:
            result.append(self.value())
            if self.peek() == ']': self.consume(']'); return result
            self.consume(',')

    def literal(self, word, value):
        for c in word:
            if self.pos >= len(self.text) or self.text[self.pos] != c:
                raise JSONError(f"Expected '{word}' at {self.pos}")
            self.pos += 1
        return value

def serialize(obj, indent=0, level=0):
    sp = " " * indent; nsp = " " * indent * (level + 1); csp = " " * indent * level
    if obj is None: return "null"
    if isinstance(obj, bool): return "true" if obj else "false"
    if isinstance(obj, int): return str(obj)
    if isinstance(obj, float): return f"{obj:g}"
    if isinstance(obj, str):
        s = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
        return f'"{s}"'
    if isinstance(obj, list):
        if not obj: return "[]"
        items = [f"{nsp}{serialize(v, indent, level+1)}" for v in obj]
        sep = ",\n" if indent else ", "
        return f"[\n{sep.join(items)}\n{csp}]" if indent else f"[{sep.join(i.strip() for i in items)}]"
    if isinstance(obj, dict):
        if not obj: return "{}"
        items = [f'{nsp}{serialize(k, indent, level+1)}: {serialize(v, indent, level+1)}' for k, v in obj.items()]
        sep = ",\n" if indent else ", "
        return f"{{\n{sep.join(items)}\n{csp}}}" if indent else "{" + ", ".join(i.strip() for i in items) + "}"

def main():
    import argparse
    p = argparse.ArgumentParser(description="JSON parser from scratch")
    p.add_argument("file", nargs="?", help="JSON file (stdin if omitted)")
    p.add_argument("-v", "--validate", action="store_true", help="Validate only")
    p.add_argument("-i", "--indent", type=int, default=2, help="Indent (0=compact)")
    p.add_argument("-q", "--query", help="Simple dot-path query (e.g. 'key.0.name')")
    args = p.parse_args()
    text = open(args.file).read() if args.file else sys.stdin.read()
    try:
        obj = Parser(text).parse()
        if args.validate: print("✅ Valid JSON"); return
        if args.query:
            for part in args.query.split("."):
                try: obj = obj[int(part)]
                except (ValueError, TypeError): obj = obj[part]
        print(serialize(obj, args.indent))
    except JSONError as e: print(f"❌ Invalid JSON: {e}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__": main()
