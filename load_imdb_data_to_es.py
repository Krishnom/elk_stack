# data.tsv can be obtained from https://www.imdb.com/interfaces/ 
# Get title.basics.tsv.gz file and untar. the untarred file can directly be fed to this script.



import json
import requests
import threading



def upload_json(id,data, index):
    header = {"Content-Type":"application/json"}
    elk_resp = requests.post(url=f"http://172.19.64.87:9200/{index}/_doc/{id}", json=data, headers=header)
    print(elk_resp.json())


def process_entry(entry):
    #tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
    data = entry.split("\t")

    #We are not interested in anything other than movie
    if data[1] != "movie":
        # print(f"{data[2]} is Not a movie")
        return

    id = data[0]
    title = data[2]
    year = data[5]
    genres = data[8]

    payload = {
        "title":title,
        "year":year,
        "genre":genres
    }
    upload_json(id, payload, "movie_db")
    pass

max_thread = 10
process_t = list(range(max_thread))
entries=[]
entry_count=0
# # using utf8 to fix "UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 1655: character maps to <undefined>"
# for entry in open("D:\\workspace\\learnings\\github-repos\\elk_stack\\data.tsv", 'r', encoding="utf8"):
#     #print(entry)
    # process_t(entry)
#     pass

with  open("D:\\workspace\\learnings\\github-repos\\elk_stack\\data.tsv", 'r', encoding="utf8") as file:
    entries = file.read()
    entries = entries.split("\n")

while entry_count <= (len(entries) + max_thread):
    for i in range(max_thread):
        entry = entries[entry_count+i]
        # print(entry)
        process_t[i] = threading.Thread(target=process_entry, args=(entry,))
        process_t[i].start()

    entry_count += max_thread

    for i in range(max_thread):
        process_t[i].join()
        pass



def movies_to_json():
        file = open("D:\\workspace\\learnings\\github-repos\\elk_stack\\data.tsv", 'r')
