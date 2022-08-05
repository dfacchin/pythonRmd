def remove_values_from_list(the_list, key, val):
   return [value for value in the_list if value[key] != val]

a = [ { "nome":"lele","cognome":"facchin"},
      { "nome":"alessia","cognome":"facchin"},
      { "nome":"diego","cognome":"facchin"},
      { "nome":"marina","cognome":"oneglio"}]

c = remove_values_from_list(a,"cognome","facchin")
print(c)