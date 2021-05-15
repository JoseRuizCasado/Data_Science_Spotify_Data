with open('data.json', 'r') as data:
    content = data.read()
    content = content.strip('[').strip(']').replace('}, ', '}\n')

with open('data_mongo.json', 'w') as out:
    out.write(content)
