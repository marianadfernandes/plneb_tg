import re
import json

file = open('output1.xml', encoding='UTF-8')
text = file.read()
file.close()

# apanhar tudo o que está entre tags de texto
text = re.sub(r'<text\b[^>]*>(.*?)</text>', r'\1', text)

# apagar todo o texto até começar o dicionário português-inglês-espanhol (1º termo)
index = text.find("<b>à morte (bras.)</b>")
if index != -1:
    text = text[index:]

# apagar blocos repetidos que correspondem à barra lateral português-inglês-espanhol
text = re.sub(r'<b>português<\/b>[\s\S]*?<b>espanhol<\/b>', '', text)

# apagar desde tag para número da página até fim de página (inclui termo que repete no inicio e fim da página - bug)
text = re.sub(r'<b>\d+(.*\n)+?<\/page>', '', text)

# apanhar as tags de inicio de página e fontspec
text = re.sub(r'<page.*(\n\s.*)?', '', text)
# apagar as letras que identificam as secções do dicionário (A, B, C,...)
text = re.sub(r'<b>[A-Z]</b>', '', text)
# apagar os distintivos de feminino, masculino, plural, adj, adv,...
text = re.sub(r'<i>\(?.*\)?</i>', '', text)


# substituir todas as sequências de \n por apenas um só
text = re.sub(r'\n\n+', r'\n', text)

# corrigir casos em que o ) ficou fora da tag do termo
text = re.sub(r'</b>\n\)', r')</b>', text)

# apanhar termos (designações) com mais do que uma linha e juntá-los numa só expressão <b>termo</b>
text = re.sub(r'(<b>.+</b>\n)+',
              lambda match: f'<b>{" ".join(re.findall(r"<b>(.+?)</b>", match.group(0)))}</b>\n', text)

# apanhar traduções com mais do que uma linha, incluindo casos em que a mudança de linha é depois de uma vírgula
text = re.sub(r'([a-z]+,? ?.*)((?:\n[^A-Z<].*)+)',
              lambda match: match.group(1) + match.group(2).replace("\n", " "), text)

# juntar palavras separadas por "mudança de linha"
text = re.sub(r'-\s', r'', text)


# corrigir casos em que o termo está partido fora da sua tag (bloqueador-B)
text = re.sub(r'-</b> (.)', r'-\1</b>', text)
# corrigir casos em que a descrição está partida por carateres diferentes (B-bloqueante)
text = re.sub(r'\s-', r'-', text)


# apagar casos em que ficam () sem conteúdo no meio, porque teriam adj, adv, etc... ou casos em que tem (adj.) no termo
text = re.sub(r'\((adj.)? .*?\)', '', text)


# resolução de casos especiais onde a tradução estava partida por outras razões: mudança de linha depois de uma vírgula; segunda parte começa com letra maiúscula
text = re.sub(r',\n([^EU]\w)', r', \1', text)
text = re.sub(r'([a-z])\n([^EU(<b]\w)', r'\1 \2', text)


# eliminação de um termo repetido no inicio e fim da página que não ficou depois do número da página mas sim antes, por isso não tinha sido apanhado anteriormente
text = re.sub(r'<b>coçar</b> ', '', text)


# ------------------------------------------------------------------------------------------------------

# obtenção das entries do dicionário
entries = re.findall(
    r'<b>(.*)</b>\nU\n(.*)\nE\n(.*)', text)

# ------------------------------------------------------------------------------------------------------

# formatação das entries
new_entries = [(designation, ({"en": description1, "es": description2}))
               for designation, description1, description2 in entries]

dic = dict(new_entries)

# ------------------------------------------------------------------------------------------------------

# verificação dos comprimentos do dicionário e das entries obtidas, para ver se se perdeu algum termo por repetição
print(len(dic))
print(len(entries))

# termos que estavam repetidos - têm duas entradas no pdf original
entries_first_element = [tpl[0] for tpl in entries]

repeated_words = []
seen_words = set()
for word in entries_first_element:
    if word in seen_words and word not in repeated_words:
        repeated_words.append(word)
    else:
        seen_words.add(word)

print(repeated_words)

# ------------------------------------------------------------------------------------------------------

txt = open('alterado2.xml', 'w', encoding='UTF-8')
txt.write(text)
txt.close()

out = open('dicionario_obrigatorio.json', 'w', encoding='UTF-8')
json.dump(dic, out, ensure_ascii=False, indent=4)
out.close()
