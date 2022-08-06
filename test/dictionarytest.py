
dic = [ {"Nome":"Daniele", "Cognome":"Facchin","eta":41},
        {"Nome":"Ezio", "Cognome":"Facchin","eta":75},
        {"Nome":"Gemma", "Cognome":"Bee","eta":64},
        {"Nome":"Fabio", "Cognome":"Facchin","eta":43},
        {"Nome":"Stefano", "Cognome":"Facchin","eta":34},
        {"Nome":"Diego", "Cognome":"Facchin","eta":10},
        {"Nome":"Alessia", "Cognome":"Facchin","eta":12},
        {"Nome":"Marina", "Cognome":"Oneglio","eta":40}
    ]

print( max(dic, key=lambda x:x['eta']) )
el = max(dic, key=lambda x:x['eta'])
dic.pop(dic.index(el))

