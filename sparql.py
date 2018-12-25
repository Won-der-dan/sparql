import json
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

recommendFilm = 'Whiplash'

def get_films(recommendFilmUri):
    query = """SELECT ?filmLabel ?cost WHERE {
  ?film wdt:P31 wd:Q11424.
  ?film wdt:P2130 ?cost.
  ?selectedfilm wdt:P2130 ?selectedcost.
  filter(?selectedfilm= wd:Q15648198 && ?cost> ?selectedcost)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


films = requests.get('https://www.wikidata.org/w/api.php', {
    'action': 'wbgetentities',
    'titles': recommendFilm,
    'sites': 'enwiki',
    'props': '',
    'format': 'json'
}).json()
recommendFilmUri = list(films['entities'])[0]
results = get_films(recommendFilmUri)
filmsArray = []
for result in results["results"]["bindings"]:
    filmsArray.append(result["filmLabel"]["value"])
json_file = dict()
json_file[recommendFilmUri] = filmsArray
with open('result.json', 'w') as outfile:
    json.dump(json_file, outfile, indent=4);
