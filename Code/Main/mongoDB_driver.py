import certifi
import pymongo
from bson.objectid import ObjectId
import json
from pymongo import ASCENDING, DESCENDING

##########################################################
# CONNECT TO MONGODB w/ DRIVER
##########################################################
def connectMongoDB():
    ca = certifi.where()
    username = "toddgavin"
    password = "XGiMOhZ1XMCpxMJX"
    uri = f"mongodb+srv://{username}:{password}@cluster0.u0ixrbx.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(uri, tlsCAFile=ca)
    db = client.test

    try:
        client.admin.command('ping')
        print("Log: Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Error connecting.")
        print(e)

    return client

##########################################################
# DEFINE DB, COLLECTION, AND DOCUMENT FILTER
##########################################################

def db_collection_document(client, db_name, collection_name, objectId):

    # get a reference to the database
    db = client[db_name]

    # get a reference to the collection
    collection = db[collection_name]

    # define the filter to match the document with a specific _id
    documentFilter = {'_id': ObjectId(objectId)}

    return db, collection, documentFilter

#############################
# GET
#############################

# Sort by numbers, than letters, than special characters, and then finally datatype
def custom_sort_key(item):
    key = list(item.keys())[0]
    if key.isdigit():
        return (0, int(key))
    elif key.isalpha():
        return (1, key)
    elif isinstance(list(item.values())[0], (dict, list, tuple)):
        return (3, key)
    else:
        return (2, key)
    
def helper_filter(data, filter_params):

    data_list = [{"{}".format(key): value} for key, value in data.items()]
    data_values_list = [data[key] for key in data]
    final_list = []

    print(f"Log monogDB_driver.py: data_list = {data_list}")
    print(f"Log monogDB_driver.py: data_values_list = {data_values_list}")
    print(f"Log monogDB_driver.py: filter_params = {filter_params}")
    
    # if orderBy is NOT in filter_params BUT other filter params are, return error
    if 'orderBy' not in filter_params and len(filter_params) > 0:
        # curl -X GET 'http://127.0.0.1:5000/users.json?equalTo=age'
        return {"error" : "orderBy must be defined when other query parameters are defined"}
    
    else:
        if 'limitToFirst' in filter_params and 'limitToLast' in filter_params:
            # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&limitToFirst=2&limitToLast=3'
            return {"error" : "Only one of limitToFirst and limitToLast may be specified"}
        
        if 'equalTo' in filter_params and ('startAt' in filter_params or 'endAt' in filter_params or 'startAfter' in filter_params or 'endBefore' in filter_params):
            # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102&startAt=13'
            return {"error" : "equalTo cannot be specified in addition to startAfter, startAt, endAt, or endBefore"}

        orderBy = filter_params.get('orderBy')
        if orderBy == "$key":
            orderBy_list = sorted(data_list, key=custom_sort_key)
            final_list = orderBy_list
            print(f"Log monogDB_driver.py: orderBy_list = {orderBy_list}")
        elif orderBy == "$value":
            orderBy_list = sorted(data_values_list, key=custom_sort_key)
            final_list = orderBy_list
            print(f"Log monogDB_driver.py: orderBy_list = {orderBy_list}")
        else:
            # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="name"'
            return {"error" : "Constraint key field must be a valid key name"}
        
        if 'orderBy' in filter_params and len(filter_params) == 1:
            print(f"Log monogDB_driver.py: completed orderBy WITHOUT addtional parameters")
            return final_list
        
        if ('startAt' not in filter_params and 'endAt' not in filter_params and 'equalTo' not in filter_params) and ('limitToFirst' in filter_params and 'limitToLast' in filter_params):
            return final_list
        
        # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102'
        equalTo_list = []
        if 'equalTo' in filter_params:
            equalTo = filter_params.get('equalTo')
            equalTo_list = [key for key in orderBy_list if equalTo in key]
            final_list = equalTo_list
            print(f"Log monogDB_driver.py: completed equalTo WITHOUT addtional parameters")

        if ('limitToFirst' not in filter_params and 'limitToLast' not in filter_params) and ('startAt' not in filter_params and 'endAt' not in filter_params):
            print(f"Log monogDB_driver.py: returning final_list WITHOUT limitToFirst, limitToLast, startAt, and endAt")
            return final_list
        
        else:
            # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106'
            startAt_list = []    
            if 'startAt' in filter_params:
                startAt = filter_params.get("startAt")

                print(f"Log monogDB_driver.py: startAt = {startAt}")

                flag = False
                for item in final_list:
                    item_key = next(iter(item))
                    print(f"Log monogDB_driver.py: item_key = {item_key}")

                    # if (str(item_key) == str(startAt) or float(item_key) >= float(startAt)) and flag == False:

                    # if (str(item_key) == str(startAt) or (isinstance(item_key, (int, float)) and float(item_key) >= float(startAt))) and flag == False:
                    #     flag = True
                    #     startAt_list.append(item)
                    # elif flag == True:
                    #     startAt_list.append(item)

                    try:
                        item_key = float(item_key)
                        if (str(item_key) == str(startAt) or item_key >= float(startAt)) and flag == False:
                            flag = True
                            startAt_list.append(item)
                        elif flag == True:
                            startAt_list.append(item)

                        print(f"Log monogDB_driver.py: ran try..")

                    except:
                        if (str(item_key) == str(startAt)) and flag == False:
                            flag = True
                            startAt_list.append(item)
                        elif flag == True:
                            startAt_list.append(item)

                        print(f"Log monogDB_driver.py: ran except..")

                final_list = startAt_list

                print(f"Log monogDB_driver.py: startAt_list = {startAt_list}")

            endAt_list = [] 
            if 'endAt' in filter_params:
                endAt = filter_params.get("endAt")

                print(f"Log monogDB_driver.py: endAt = {endAt}")

                flag = False
                for item in final_list:
                    item_key = next(iter(item))
                    print(f"Log monogDB_driver.py: item_key = {item_key}")
                    
                    # if (str(item) != str(endAt) or float(item) <= float(endAt)) and flag == False:
                    try:
                        item_key = float(item_key)
                        if (str(item_key) == str(endAt) or item_key >= float(endAt)) and flag == False:
                            flag = True
                            print("RAN1")
                        elif flag == False:
                            endAt_list.append(item)
                            print("RAN2")

                        print(f"Log monogDB_driver.py: ran try..")
                        
                    except:
                        if (str(item_key) == str(endAt)) and flag == False:
                            flag = True
                            print("RAN1")
                        elif flag == False:
                            endAt_list.append(item)
                            print("RAN2")

                        print(f"Log monogDB_driver.py: ran except..")

                final_list = endAt_list

                print(f"Log monogDB_driver.py: endAt_list = {endAt_list}")

        print(f"Log monogDB_driver.py: completed startAt and endAt")

        # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToFirst=2'
        if 'limitToFirst' in filter_params:
            limitToFirst = filter_params.get("limitToFirst")

            print(f"Log monogDB_driver.py: limitToFirst = {limitToFirst}")

            limitToFirst_int = int(limitToFirst) if limitToFirst.isdigit() else {"error" : "limitToFirst must be an integer"}

            print(f"Log monogDB_driver.py: limitToFirst_int = {limitToFirst_int}")

            if isinstance(limitToFirst_int, dict):
                return limitToFirst_int

            if len(final_list) > limitToFirst_int:
                return final_list[:limitToFirst_int]
            else:
                return final_list
            
        # curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToLast=2'
        elif 'limitToLast' in filter_params: 
            limitToLast = filter_params.get("limitToLast")

            print(f"Log monogDB_driver.py: limitToLast = {limitToLast}")

            limitToLast_int = int(limitToLast) if limitToLast.isdigit() else {"error" : "limitToLast must be an integer"}

            print(f"Log monogDB_driver.py: limitToLast_int = {limitToLast_int}")

            if isinstance(limitToLast_int, dict):
                return limitToLast_int
            
            if len(final_list) > limitToLast_int:
                return final_list[-limitToLast_int:]
            else:
                return final_list
            
        else:
            print(f"Log monogDB_driver.py: completed WITHOUT limitToFirst and limitToLast")
            return final_list
        
def get(collection, documentFilter, jsonPath, filter=None):

    print(f"Log flaskApp_RESTfulServer.py: Starting GET...")
    
    if jsonPath == '':
        result = list(collection.find(documentFilter))[0]
    else: 
        result = collection.find(documentFilter).distinct(jsonPath)[0]

    print(f"Log flaskApp_RESTfulServer.py: Starting GET Filter...")

    if filter is None:

        print(f"Log flaskApp_RESTfulServer.py: There is NO Filter in this request")

        return result
    else:
        filtered_result = helper_filter(result, filter)
        return filtered_result

#############################
# PUT
#############################
def helper_Update_PUT(data, jsonPath):

    updates = {}

    for key, value in data.items():
        if jsonPath == '':
            newKey = f"{key}"
        else:
            newKey = f"{jsonPath}.{key}"
        updates[newKey] = value

    update = {'$set': updates}
    # print(update)
    return update

def put(collection, documentFilter, jsonPath, data):
    update = helper_Update_PUT(data, jsonPath)
    # print(update)
    collection.update_one(documentFilter, update)

#############################
# POST
#############################
def helper_Update_POST(data, jsonPath):

    updates = {}
    unique_key = str(ObjectId())

    if jsonPath == '':
        jsonPath = f"{unique_key}"
    else:
        jsonPath = f"{jsonPath}.{unique_key}"

    for key, value in data.items():
        newKey = f"{jsonPath}.{key}"
        updates[newKey] = value

    # uniqueKeyUpdates = {}
    # uniqueKeyUpdates[unique_key] = updates

    update = {'$set': updates}
    print(update)
    return update

def post(collection, documentFilter, jsonPath, data):
    update = helper_Update_POST(data, jsonPath)
    collection.update_one(documentFilter, update)

#############################
# PATCH
#############################

# PATCH either writes data if it doesnt exist or rewrites the data if it does exist
def patch(collection, documentFilter, jsonPath, data):
    # get the current json within the jsonPath and rewrite/add the data

    currentData = get(collection, documentFilter, jsonPath, None)
    merged_data = currentData.copy()
    merged_data.update(data)

    print(currentData)
    print(data)
    print(merged_data)

    put(collection, documentFilter, jsonPath, merged_data)

#############################
# DELETE
#############################
def delete(collection, documentFilter, jsonPath):
    update = {'$unset': {jsonPath: 1}}
    collection.update_one(documentFilter, update)