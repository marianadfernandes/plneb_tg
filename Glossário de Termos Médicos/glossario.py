import re 
import json

with open("Glossário de Termos Médicos Técnicos e Popularess.html", "r", encoding="UTF8") as f:
    lines = f.readlines()

# retirar marcas não necessárias do texto 
text = ''
for line in lines:
    line = re.sub(r'&#160;', r' ', line)
    line = re.sub(r'</?a.*?>', r'', line)
    line = re.sub(r'[A-Z]?<br/>', r'', line)
    line = re.sub(r'<hr/>', r'', line)
    line = re.sub(r'[ ]+', r' ', line)
    line = re.sub(r'&#34;', r"'", line)
    text += line

# corrigir situações onde a expressão está separada
text = re.sub(r'\n\n\(', r'\(', text)
text = re.sub(r'<\/i>\s+<i>', r' ', text)

with open('glossario_limpo.txt', 'w', encoding="UTF8") as f:
    f.write(text)

# 1º capturar linhas que estão exp popular -> termo
entries1 = re.findall(r'<i>(.*)<\/i>(?:.*)<b>(.+)<\/b>', text)

# inverter o dicionario dado que estava ao contrário da ordem pretendida (termo -> ex popular)
dic = {termo2 : termo1 for termo1, termo2 in entries1}

with open('glossario1.json', 'w', encoding="UTF8") as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)

# 2º capturar as linhas que estão termo - exp popular
entries2 = re.findall(r'<b>(.+)<\/b>(?:.*)<i>(.*)<\/i>', text)

# adicionar ao dicionario com os outros termos já captados antes
for termo, exp in entries2:
    dic[termo.strip()] = exp.strip()

# ordenar o dicionário por ordem alfabética
dic = sorted(dic.items())

with open('glossario_final.json', 'w', encoding="UTF8") as f:
    json.dump(dict(dic), f, ensure_ascii=False, indent=4)