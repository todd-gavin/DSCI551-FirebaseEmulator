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
def helper_filter(collection, orderBy=None, limitToFirst=None, limitToLast=None, equalTo=None, startAt=None, endAt=None):
    filter = {}
    sort_order = None
    limit = None  # Initialize limit variable here

    if orderBy:
        if orderBy == '$key':
            key = '_id'
        elif orderBy == '$value':
            raise ValueError("orderBy '$value' not supported. Please use a specific field name.")
        else:
            key = orderBy
            # Create index for the orderBy field
            collection.create_index([(key, ASCENDING)])

        if startAt is not None:
            filter[f'{key}'] = {'$gte': startAt}

        if endAt is not None:
            if f'{key}' in filter:
                filter[f'{key}']['$lte'] = endAt
            else:
                filter[f'{key}'] = {'$lte': endAt}

        if equalTo is not None:
            filter[f'{key}'] = equalTo

        if limitToFirst is not None and orderBy:
            limit = limitToFirst
            sort_order = ASCENDING
        elif limitToLast is not None:
            limit = limitToLast
            sort_order = DESCENDING

    return filter, limit, sort_order


def get(collection, documentFilter, jsonPath, filter=None):
    if filter is None:
        if jsonPath == '':
            result = list(collection.find(documentFilter))
        else: 
            result = collection.find(documentFilter).distinct(jsonPath)
    else:
        filter, limit, sort_order = helper_filter(collection, **filter)
        if jsonPath == '':
            if sort_order is not None:
                result = list(collection.find({'$and': [documentFilter, filter]}).sort('_id', sort_order).limit(limit))
            else:
                result = list(collection.find({'$and': [documentFilter, filter]}))
        else:
            if sort_order is not None:
                result = collection.find({'$and': [documentFilter, filter]}).sort('_id', sort_order).distinct(jsonPath)[:limit]
            else:
                result = collection.find({'$and': [documentFilter, filter]}).distinct(jsonPath)
    return result


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

    currentData = get(collection, documentFilter, jsonPath, None)[0]
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