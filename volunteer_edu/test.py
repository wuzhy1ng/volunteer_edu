import json

tt = {'name': 'hello', 'age': 16}
json_str = json.dumps(tt)
json_data = json.loads(json_str)

print(json_str)
print(json_data)
