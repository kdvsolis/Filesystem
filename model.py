import pymongo
from datetime import datetime
import random
from pprint import pprint

class Model:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]

    def new_folder(self, userID, main_folder):
        foldercol = self.mydb["folders"]
        placeholder = {
                        "folder": main_folder,
                        "userID":userID
                    }
        data_to_insert = {
                            "$setOnInsert" : {  
                                "userID": userID,
                                "folder": main_folder,
                                "timestamp": datetime.now()
                            }
                        }
        foldercol.update_one(placeholder, 
                            data_to_insert,
                            True)
        return {"userID" : userID, "folder" : main_folder}

    def new_subfolder(self, userID, main_folder, subfolder):
        foldercol = self.mydb["folders"]
        subfoldercol = self.mydb["subfolder"]
        placeholder = {
                        "userID": userID,
                        "folder": main_folder,
                        "subfolder": subfolder
                    }
        data_to_insert = {
                            "$setOnInsert" : { 
                                "userID": userID,
                                "folder": main_folder,
                                "subfolder": subfolder,
                                "timestamp": datetime.now()
                            }
                        }
        if(foldercol.find({"userID" : userID, "folder" : main_folder}).limit(1).count() == 1):           
            subfoldercol.update_one(placeholder, 
                                data_to_insert,
                                True)
            return { "status" : "success" }
        return { "status" : "inexistent root folder" } 

    def get_folder_content(self, userID, folder_limit, subfolder_limit):
        folder_list = []
        foldercol = self.mydb["folders"]
        subfoldercol = self.mydb["subfolder"]
        folder_result = foldercol.find({"userID": userID}, { "_id": 0, "userID": 1, "folder": 1 })
        if(isinstance(folder_limit, int)):
            folder_result = folder_result.limit(folder_limit)
        for f in folder_result:
            folder_list.append(f["folder"])
            sub_folder_result = subfoldercol.find({"userID": userID, "folder": f["folder"]}, { "_id": 0, "userID": 1, "folder": 1, "subfolder": 1})
            if(isinstance(subfolder_limit, int)):
                sub_folder_result = sub_folder_result.limit(subfolder_limit)
            for s in sub_folder_result:
                folder_list.append(f["folder"] + "/" + s["subfolder"])
                
        return folder_list

    def get_folder_count(self, userID):
        folder_count = 0
        foldercol = self.mydb["folders"]
        subfoldercol = self.mydb["subfolder"]
        folder_result = foldercol.find({"userID": userID}, { "_id": 0, "userID": 1, "folder": 1 })
        for f in folder_result:
            folder_count += subfoldercol.find({"userID": userID, "folder": f["folder"]}, { "_id": 0, "userID": 1, "folder": 1, "subfolder": 1, "timestamp": 1}).count()
        return folder_count
        
    def get_folder_sorted(self, userID, folder, limit):
    
        folder_list = []
        subfoldercol = self.mydb["subfolder"]
        
        sub_folder_result = subfoldercol.find({"userID": userID, "folder":folder}, { "_id": 0, "userID": 1, "folder": 1, "subfolder": 1, "timestamp" : 1 }).sort("timestamp", pymongo.DESCENDING)

        if(isinstance(limit, int)):
            sub_folder_result = sub_folder_result.limit(limit)
            
        for s in sub_folder_result:
            folder_list.append({"folder" : folder + "/" + s["subfolder"], "timestamp" : s["timestamp"].strftime("%m/%d/%Y, %H:%M:%S")})
        return folder_list
             
    def get_newest(self):
        foldercol = self.mydb["folders"]
        subfoldercol = self.mydb["subfolder"]
        folder_result = foldercol.find().sort("timestamp", pymongo.DESCENDING).limit(1)
        sub_folder_result = subfoldercol.find().sort("timestamp", pymongo.DESCENDING).limit(1)
        print(sub_folder_result[0]["folder"] + "/" + sub_folder_result[0]["subfolder"] + " " + sub_folder_result[0]["timestamp"].strftime("%m/%d/%Y, %H:%M:%S"))
        print(folder_result[0]["folder"] + " " + folder_result[0]["timestamp"].strftime("%m/%d/%Y, %H:%M:%S"))
        if (folder_result[0]["timestamp"] > sub_folder_result[0]["timestamp"]):
            return folder_result[0]["userID"] + " " + folder_result[0]["folder"] + " " + folder_result[0]["timestamp"].strftime("%m/%d/%Y, %H:%M:%S")
        return sub_folder_result[0]["userID"] + " " + sub_folder_result[0]["folder"] + "/" + sub_folder_result[0]["subfolder"] + " " + sub_folder_result[0]["timestamp"].strftime("%m/%d/%Y, %H:%M:%S")