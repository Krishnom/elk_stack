#This requires elasticsearch module. Use "pip3 install elasticsearch"
#Download  title.basics.tsv from https://datasets.imdbws.com/title.basics.tsv.gz and execute gunzip title.basics.tsv.gz
#Run as python3 <scriptname>

import csv
import elasticsearch
from _collections import deque
from elasticsearch import helpers


def readdata():
    csvFile = open("/home/opaliwal/title.basics.tsv", 'r')

    reader = csv.DictReader(csvFile, dialect="excel-tab")
    #
    # for movie in reader:
    #     print(movie.keys())
    #     print(movie.values())
    #     print(movie.get("titleType"))
    #     break
    print("Reading complete")
    return reader


def get_movie():
    movies = readdata()
    for entry in movies:
        movie = {}
        movie['imdb_id'] = entry['tconst']
        movie['title'] = str(entry['primaryTitle'])
        movie['year'] = entry['startYear']
        movie['genre'] = entry['genres']
        yield movie


# es = elasticsearch.Elasticsearch(({"host": "172.19.64.87", "port": 9200}))
es = elasticsearch.Elasticsearch()
es.indices.delete(index='imdb_movies', ignore=404)
deque(helpers.parallel_bulk(es,get_movie(), index='imdb_movies'), maxlen=0)
es.indices.refresh()
