# Fileserver
========================
# Description

## Schema design

Root folders
{ 
    "userID": userID,
    "folder": main_folder,
    "timestamp": datetime.now()
}

Sub folders
{ 
    "userID": userID,
    "folder": main_folder,
    "subfolder": subfolder,
    "timestamp": datetime.now()
}

# Dependencies
python3
pymongo
MongoDB Compass Community


# Setup

1. Pull this repository
2. Follow the guide to install python3 from here: https://www.python.org/downloads/
3. On your terminal, do ```pip install pymongo```
4. Run server by doing ```python3 server.py```
5. Run file loader script by doing ```python3 file_generator.py```

# API Usage

Get the folder tree for a given user by id:
/userid-content/{userID}/{root-folder-limit}/{sub-folder-limit}
Where: 
   userID - target userID
   root-folder-limit - number for limit of root folders query
   sub-folder-limit - number for limit of subfolders query

Get the items counts for each folder:
/item-count/{userID}
Where: 
   userID - target userID
   
Get the items in a given folder, sorted by default by timestamp, newest first.
/folder-content/{userID}/{root-folder-limit}/{sub-folder-limit}
Where: 
   userID - target userID
   root-folder-limit - number for limit of root folders query
   sub-folder-limit - number for limit of subfolders query

Get the N newest items regardless of the folder they are in
/newest-folder