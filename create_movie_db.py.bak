See http://www.omdbapi.com/ for more details
import requests
import json
import threading

apikey="" #TODO update this apikey with your key. request your key from omdb website.

def import_movie_to_elk(movie_id):
    print(f"Retrieving movie # {movie_id}")
    resp = requests.get(f"http://www.omdbapi.com/?i=tt{movie_id}&apikey={apikey}")
    if resp.status_code != 200:
        print (f"# {movie_id} - Something went wrong:  {resp.status_code}" )
        return

    
    resp = resp.json()
    if resp['Response'] == 'False':
        print("Something bad with response.")
        return

    if str(resp['Language']) != "English":
        print (f"Movie {resp['Title']} is {resp['Language']}. Not in English.")
        return

    if str(resp['Type']).lower() != "movie":
        print (f"# {movie_id} - {resp['Title']} is Not a movie.")
        return

    if int(resp['Year']) < 1989:
        print (f"Movie {resp['Title']} released before i was born.")
        return   

    # print(f"# {movie_id} - {resp}")
    doc = {
            "title": resp["Title"],
           "year": resp['Year'],
            "genre": resp['Genre'],
            "language": resp['Language'],
            "plot": resp['Plot'],
            "actor": resp['Actors']
        }

    header = {"Content-Type": "application/json"}
    # print(doc)
    # with open("payload.json", "w") as write_file:
    #     json.dump(doc, write_file)

    elk_resp = requests.post(url=f"http://172.19.64.87:9200/movie_db/_doc/{movie_id}", json=doc, headers=header)
    print(elk_resp.json())


movie_count = 3000
id_start=1000000
movie_t = list(range(movie_count))
for i in range(movie_count):
    movie_id = id_start + i
    movie_t[i] = threading.Thread(target=import_movie_to_elk, args=(movie_id,))
    movie_t[i].start()

for i in range(movie_count):
    movie_t[i].join()


