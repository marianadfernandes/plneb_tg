import re 
import json

with open("Glossário de Termos Médicos Técnicos e Popularess.html", "r", encoding="UTF8") as f:
    lines = f.readlines()

# retirar marcas estranhas do text
novo1 = ''
for line in lines:
    line = re.sub(r'&#160;', r' ', line)
    line = re.sub(r'</?a.*?>', r'', line)
    line = re.sub(r'[A-Z]<br/>', r'', line)
    line = re.sub(r'<hr/>', r'', line)
    novo1 += line

novo1 = re.sub(r'\n\n\(', r'\(', novo1)

with open('glossario.txt', 'w', encoding="UTF8") as f:
    f.write(novo1)


# 1º apanhar linhas que estão exp popular - termo
novo2 = re.findall(r'<i>(.*)<\/i>(?:.*)<b>(.+)<\/b>', novo1)

# inverter o dicionario pq estava ao contrário do que queriamos
novo2 = {termo2 : termo1 for termo1, termo2 in novo2}

with open('glossario2.json', 'w', encoding="UTF8") as f:
    json.dump(novo2, f, ensure_ascii=False, indent=4)

# apanhar as linhas que estão termo - exp popular
novo3 = re.findall(r'<b>(.+)<\/b>(?:.*)<i>(.*)<\/i>', novo1)

# adicionar ao dicionario com os outros termos já captudos antes
for termo, exp in novo3:
    novo2[termo] = exp

novo4 = sorted(novo2.items())

with open('glossario3.json', 'w', encoding="UTF8") as f:
    json.dump(dict(novo4), f, ensure_ascii=False, indent=4)