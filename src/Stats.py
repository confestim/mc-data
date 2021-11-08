import json
import os
import requests
import logging 
   
logger_format = '%(asctime)s:%(threadName)s:%(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")


class Stats():
    """Gets all/user data from files
       
        Parameters
        ----------

        path : Specific path of the 'stats' folder, defaults to '../stats'.
 
        user : Name of user, defaults to None => all users.

        Returns
        -------

        player_data : dict with the player(s) data.   
        
        player_names : list with the player name(s).

    """
    def __init__(self,
    path=os.path.abspath("../stats"),
    user:str=None):

        try:
            for i in os.listdir(path):
                if "-" in i:
                    new_name = i.replace("-", "")
                    os.rename("{0}/{1}".format(path, i), "{0}/{1}".format(path, new_name))
                    logging.info(f"File format of {i} corrected.")        

        except Exception as e:
            logging.info(e)
            logging.info("This usually means that your files are already corrected.")


        if user:
            uuid = requests.get(f"https://api.minetools.eu/uuid/{user}").json()["id"]
            with open("{0}/{1}.json".format(path, uuid), "r") as f:
                player = json.load(f)
            self.player_data = {user:player}
            self.player_names = user
        
        else:
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
                    logging.info(f"Non json file - {i}\nSkipping...")

            self.player_data = player_data
            self.player_names = player_names

    def get_data(
        self,
        data_type:str=None,
        data:dict=None) -> list:
        """Gets specific data for the player(s) given
        
        Parameters
        ----------

        data : player data list with json/dict, defaults to None, which leads to using the data for the user(s) given when initializing the class.
        
        data_type : string which is a choice between the different types of data contained in the stats files.

        Returns
        -------

        mined_blocks : dict with all the mined blocks and their frequency
        """
        if not data:
            data = self.player_data


        data_types = []        
        for i in data:
            for l in data[i]["stats"]:
                if l not in data_types:
                    data_types.append(l)


        if not data_type or data_type not in data_types:
            raise TypeError("\nPlease choose one of these as the data_type parameter:\n" + str(data_types))


        end_result = []

        for i in data:
            end_result.append({i: data[i]["stats"][data_type]})
        
        return end_result
