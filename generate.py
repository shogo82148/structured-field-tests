#!/usr/bin/env python

import json

def write(name, data):
    fh = open("%s-generated.json" % name, "w")
    json.dump(data, fh, indent=4, sort_keys=True)
    fh.close()

### strings
tests = []
## allowed characters
allowed_string_chars = [0x20, 0x21] + list(range(0x23, 0x5b + 1)) + list(range(0x5d, 0x7e + 1))
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x in string" % c,
      "raw": ["\"%s\"" % chr(c)],
      "header_type": "item"
    }
    if c in allowed_string_chars:
        test["expected"] = chr(c)
    else:
        test["must_fail"] = True
    tests.append(test)

## escaped characters
escaped_string_chars = [0x22, 0x5c]
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x in string" % c,
      "raw": ["\"\\%s\"" % chr(c)],
      "header_type": "item"
    }
    if c in escaped_string_chars:
        test["expected"] = chr(c)
    else:
        test["must_fail"] = True
    tests.append(test)
write('string', tests)

### identifiers
tests = []
## allowed characters
allowed_identifier_chars = list(range(0x30, 0x39 + 1)) + list(range(0x61, 0x7a + 1)) + \
    [ord(c) for c in ["_", "-", ".", ":", "%", "*", "/"]]
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x in identifier" % c,
      "raw": ["a%sa" % chr(c)],
      "header_type": "item"
    }
    if c in allowed_identifier_chars:
        test["expected"] = "a%sa" % chr(c)
    else:
        test["must_fail"] = True
    tests.append(test)
## allowed starting characters
allowed_identifier_start_chars = list(range(0x61, 0x7a + 1))
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x starting an identifier" % c,
      "raw": ["%sa" % chr(c)],
      "header_type": "item"
    }
    if c in [0x09, 0x20]:
        test["expected"] = "a"  # whitespace is always stripped.
    elif c in allowed_identifier_start_chars:
        test["expected"] = "%sa" % chr(c)
    else:
        test["must_fail"] = True
    tests.append(test)
write('identifier', tests)

### keys
tests = []
## allowed characters
allowed_key_chars = list(range(0x30, 0x39 + 1)) + list(range(0x61, 0x7a + 1)) + \
    [ord(c) for c in ["_", "-"]]
allowed_key_start_chars = list(range(0x61, 0x7a + 1))
## dictionary keys
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x in dictionary key" % c,
      "raw": ["a%sa=1" % chr(c)],
      "header_type": "dictionary"
    }
    if c in allowed_key_chars:
        key = "a%sa" % chr(c)
        test["expected"] = {key: 1}
    else:
        test["must_fail"] = True
    tests.append(test)
## allowed dictionary key starting characters
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x starting an dictionary key" % c,
      "raw": ["%sa=1" % chr(c)],
      "header_type": "dictionary"
    }
    if c in [0x09, 0x20]:
        test["expected"] = {"a": 1}  # whitespace is always stripped.
    elif c in allowed_identifier_start_chars:
        test["expected"] = {"%sa" % chr(c): 1}
    else:
        test["must_fail"] = True
    tests.append(test)
## param-list keys
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x in param-list key" % c,
      "raw": ["foo; a%sa=1" % chr(c)],
      "header_type": "param-list"
    }
    if c in allowed_key_chars:
        key = "a%sa" % chr(c)
        test["expected"] = [["foo", {key: 1}]]
    else:
        test["must_fail"] = True
    tests.append(test)
## allowed param-list key starting characters
for c in range(0x00, 0x7f + 1):
    test = {
      "name": "0x%02x starting a param-list key" % c,
      "raw": ["foo; %sa=1" % chr(c)],
      "header_type": "param-list"
    }
    if c in [0x09, 0x20]:
        test["expected"] = [["foo", {"a": 1}]]  # whitespace is always stripped.
    elif c in allowed_identifier_start_chars:
        test["expected"] = [["foo", {"%sa" % chr(c): 1}]]
    else:
        test["must_fail"] = True
    tests.append(test)
write('key', tests)

