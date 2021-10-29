import json
import os
import requests


def get_files(path=os.path.abspath("stats")):
    players = {}
    print(os.listdir(path))

    for i in os.listdir(path):

        if ".json" in i:
            with open(f"{path}/{i}", "r") as f:
                
                player = json.load(f)
                player_name = i.strip(".json")
                player_name = requests.get(f"https://api.minetools.eu/uuid/{player_name}").json()["name"]
                players[f"{player_name}"] = player
        else:
            print(f"Non json file - {i}\nSkipping...")
    
    return players


def get_all_names(path=os.path.abspath("stats")):
    player_names = []

    for i in os.listdir(path):
        if ".json" in i:
            with open(f"{path}/{i}", "r") as f:
                
                player_name = i.strip(".json")
                player_names.append(requests.get(f"https://api.minetools.eu/uuid/{player_name}").json()["name"])
        else:
            print(f"Non json file - {i}\nSkipping...")
    
    return player_names


def most_mined(name, limit=10, data=get_files()):

    if not name in data.keys():

        raise NameError(f"No '{name}' in the files. Try changing the config.")

    all_mined = data[name]["stats"]["minecraft:mined"]
    sorted_mined = dict(sorted(all_mined.items(), key=lambda x:x[1], reverse=True))
    result = {name:{f"top_{limit}":{}}}
    counter = 0
    
    for i in sorted_mined.keys():

        if counter >= limit:
            break
        counter += 1
        result[name][f"top_{limit}"][i] = all_mined[i]

    return result



all_names = get_all_names()
fetching_once = get_files()

for i in all_names:
    print(f"THIS IS THE DATA FORRRRR {i}!~!!!!!!\n\n\n\n\n{most_mined(i,data=fetching_once, limit=50)}")
        

  