import json
import os
import requests



class Stats():

    def __init__(self, path=os.path.abspath("../stats")):
        
        player_data, player_names = {}, []
    
        for i in os.listdir(path):

            if ".json" in i:
                with open(f"{path}/{i}", "r") as f:
                    
                    player = json.load(f)
                    player_name = i.strip(".json")
                    player_name = requests.get(f"https://api.minetools.eu/uuid/{player_name}").json()["name"]
                    player_names.append(player_name)
                    player_data[f"{player_name}"] = player
        
            else:
                print(f"Non json file - {i}\nSkipping...")

        self.player_data = player_data
        self.player_names = player_names
        
    def top(self, name, limit=10) -> dict:
        """This returns the top(10) blocks that a given user has mined"""
        data = self.player_data

        if not name in data.keys():
            raise NameError(f"No '{name}' in the files. Try changing the config.")
        
        result = {}

        all_data = data[name]["stats"]

        for a in all_data: 
            
            sorted_list = dict(sorted(all_data[a].items(),key=lambda x:x[1], reverse=True))
            
            counter = 0
            
            for i in sorted_list.keys():
                if counter >= limit:
                    break
                # result[i][a][counter] = sorted_list[i]
                result[a] = {i:{}}
                result[a][i] = {counter:sorted_list[i]}     
                # result[i][a][counter] = sorted_list[i]
                counter += 1

        return result

a = Stats()
user = a.top("turbox123")
print(user)