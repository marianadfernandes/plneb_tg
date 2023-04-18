import re
import json

with open ("WIPOPearl_COVID-19_Glossary.xml","r", encoding="UTF8") as file:
    lines = file.read()


# Remover
lines = re.sub(r"</?text.*?>", "",lines)
lines = re.sub(r"</?page.*>", "", lines)
lines = re.sub(r'(<b> </b>)?<\/?i.*?>', "", lines)
lines = re.sub(r'<fontspec[^>]*>',"", lines)

#eliminar todo o texto até à página em que começa o glossário
eliminar = lines.find('<b>A </b>')
if eliminar != -1:
    lines=lines[eliminar:]

lines= re.sub(r"<b>[A-Z] </b>", "", lines)


lines = re.sub(r'\n', "", lines)
lines = re.sub(r'COVID-19 Glossary\s+\d+', "", lines)

# eliminar desde tradução àrabe até tradução francesa (exclusive)
lines = re.sub(r'<b>\s*AR\s*</b>.*?(<b>F)', r'\1', lines)

# eliminar tradução japonesa e coreana
lines = re.sub(r'<b>\s*JA\s*</b>.*?(<b>P)', r'\1', lines)

# fica-se com: termo, descrição, tradução FR, tradução PT, tradução RU e tradução ZH

# eliminar tradução russa e zh
lines = re.sub(r'<b>\s*RU\s*</b>.*?(<b>[a-z])', r'\1', lines)

# fica-se com: termo, descrição, tradução FR e tradução PT

# eliminar lixo que permanece no documento original, como <b> </b> a separar frases
lines = re.sub(r'<b> </b>', r' ', lines)
lines = re.sub(r'</b><b>', r'', lines)

# eliminar os sinónimos quer nos termos quer nas descrições/traduções
# utilização de OU lógico "|"
lines = re.sub(r',?\s?\(syn\.\).*?\s+([A-Z][a-z]|<b>)', r'\1', lines) 

# eliminar o que está depois das traduções e antes do termo seguinte (ex: MEDI, ...)
lines = re.sub(r'\.\s+[A-Z].*?<', r'. <', lines)
lines = re.sub(r'<b>MEDI.*?(<b)', r'\1', lines)

#corrigir simbolos
lines = re.sub(r'&gt;', r'>', lines)
lines = re.sub(r'&lt;', r'<', lines)



alt = open("alterado.xml", "w", encoding="UTF8")
alt.write(lines)
alt.close()


# obtenção dos tuplos para posterior criação do dicionário
entries = re.findall(r"<b>\s*(.*?)\s*<\/b>(.*?)<b>FR\s*<\/b>\s*(.*?)\s*<b>PT\s*<\/b>\s*(.*?)(?=<b>|\Z)", lines, re.DOTALL)

entries = [(term.strip(), desc.strip(), es.strip().rstrip(), pt.strip().rstrip()) for term, desc, es, pt in entries]


# formatação das entries para o dicionário
new_entries = [(designation, ({"desc": description1, "fr": description2, "pt": description3}))
                for designation, description1, description2, description3 in entries]

dic = dict(new_entries)
         
with open('glos.json', 'w', encoding="UTF8") as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)
