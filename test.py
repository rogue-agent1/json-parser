from json_parser import parse_json
assert parse_json("42") == 42
assert parse_json("-3.14") == -3.14
assert parse_json('"hello"') == "hello"
assert parse_json("true") == True
assert parse_json("null") == None
assert parse_json("[1,2,3]") == [1,2,3]
obj = parse_json('{"a": 1, "b": [true, null, "x"]}')
assert obj == {"a": 1, "b": [True, None, "x"]}
assert parse_json('{"nested": {"key": "val"}}')["nested"]["key"] == "val"
assert parse_json('"hello\\nworld"') == "hello\nworld"
print("json_parser tests passed")
