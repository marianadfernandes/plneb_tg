import json
from deep_translator import GoogleTranslator

# ver contacto/contato

with open('Glossário de Termos Médicos/glossario_final.json', encoding="utf8") as file:
    exps = dict(json.load(file))

with open('WIPOPearl_COVID-19_Glossary/glos.json', encoding="utf8") as file:
    covid_original = dict(json.load(file))

with open('dicionario_obrigatorio.json', encoding="utf8") as file:
    obg = dict(json.load(file))
    
# formatação do dicionário glossário de expressões de populares
for key, value in exps.items():
    exps[key] = {"exp pop" : value}

# formatação do dicionário de covid - chave em pt
covid = {}

for key, value in covid_original.items():
    pt_value = value.pop("pt")
    value["en"] = key
    covid[pt_value] = value

print(covid)

# cópia do dicionário glossário de expressões de populares
exps_copia = {}
for key, value in exps.items():
  exps_copia[key] = value

# interseção de dicionario exp pop com covid 
exps_covid = {}
count = 0
for key, value in covid.items():
    if (key in exps.keys()):
        count += 1
        exps_covid[key] = {"desc_pt" : value['desc_pt'],
                    "exp pop" : exps[key]['exp pop'],
                    "en" : key,
                    "desc_en": value['desc_en'],
                    "fr" : value['fr']}
        
print(count)

with open('int_3.json', 'w', encoding="utf8") as file:
    json.dump(exps_covid, file, ensure_ascii=False, indent=4)

# interseção do dicionário de expressões populares com o das traduções en_pt
exps_enpt = {}     
count = 0
for key, value in exps.items():
    if key in obg.keys():
        count += 1
        exps_enpt[key] = {"exp pop" : value['exp pop'],
                     "en" : obg[key]['en'],
                     "es" : obg[key]['es']}
        
print(count)
        
with open('int_exps_enpt.json', 'w', encoding="utf8") as file:
    json.dump(exps_enpt, file, ensure_ascii=False, indent=4)

# interseção do dicionário de covid com o das traduções en_pt
covid_enpt = {}  
count = 0   
for key, value in covid.items():
    if key in obg.keys():
        count += 1
        covid_enpt[key] = {"desc_pt" : value['desc_pt'],
                    "en" : obg[key]['en'],
                    "desc_en": value['desc_en'],
                    "es" : obg[key]['es'],
                    "fr" : value['fr']}
        
print(count)
        
with open('int_covid_enpt.json', 'w', encoding="utf8") as file:
    json.dump(covid_enpt, file, ensure_ascii=False, indent=4)

# interseção dos três dicionários 
count = 0
for key, value in covid.items():
    if key in exps_enpt.keys():
        count += 1
        exps_enpt[key] = {"desc_pt" : covid[key]['desc_pt'],
                    "exp pop" : exps_enpt[key]['exp pop'],
                    "desc_en" : covid[key]['desc_en'],
                     "en" : exps_enpt[key]['en'],
                     "es" : exps_enpt[key]['es'],
                     "fr" : covid[key]['fr']}
        
print(count)

with open('int_3.json', 'w', encoding="utf8") as file:
    json.dump(exps_enpt, file, ensure_ascii=False, indent=4)
        
""" # união do dicionário de expressões populares com o de covid
for key, value in covid.items():
    if key in exps_copia.keys():
        exps_copia[key] = {"desc_pt" :  value['desc_pt'],
                            "exp pop": exps_copia[key]['exp pop'],
                            "en" : key,
                            "desc_en": value['desc_en'],
                            "fr" : value['fr']}
    else: 
        exps_copia[key] = {"desc_pt" :  value['desc_pt'],
                            "en" : key,
                            "desc_en": value['desc_en'],
                            "fr" : value['fr']} """
        
# exps2 = sorted(exps_copia.items())

# união do dicionário de covid com dicionario de exp populares + en_pt
dic_final = {}
count = 0
for key, value in covid.items():
    if key in exps_enpt.keys():
        count += 1
        dic_final[key] = {"desc_pt" : value['desc_pt'],
                    "exp pop" : exps_enpt[key]['exp pop'],
                    "desc_en" : value['desc_en'],
                     "en" : exps_enpt[key]['en'],
                     "es" : exps_enpt[key]['es'],
                     "fr" : value['fr']}
    else:
        count += 1
        dic_final[key] = {"desc_pt" : value['desc_pt'],
                                    "en" : value['en'],
                                    "desc_en" : value['desc_en'],
                                    "fr" : value['fr']}
        
for key, value in exps_enpt.items():
    if key not in dic_final.keys():
        count += 1
        dic_final[key] = value
        
print(count)

dic_final = sorted(dic_final.items())

with open('dicionario_final.json', 'w', encoding="utf8") as file:
    json.dump(dict(dic_final), file, ensure_ascii=False, indent=4)
