# Emulating Firebase's Realtime Database using Flask and MongoDB

## Purpose

## File Structure
- The program code is stored inside the directory `Code/Main/`
- There are two python files that work together to emulate Firebase's Realtime Database using Flask and MongoDB:
    - `flaskServer.py`: This file establishes the RESTful server to be able to listen for and accept CURL commands with GET, POST, PUT, PATCH, and DELETE.
    - `mongoDB_driver.py`: This file reads and writes data from and to the MongoDB Atlas instance.

## Implementation

## Dependencies
1. Note: This code has been tested and operated on a Apple Silicon M1 chip. Other hardware has not been tested.
2. Python Libraries:
    - flask, Flask
    - flask, request
    - json
    - certifi
    - pymongo
    - bson.objectid, ObjectId

## Run Program
1. Clone repo: `git clone <REPO LINK>`
2. Execute command inside ROOT (`$FIREBASE_EMULATOR`) of repo to start flask RESTful server: `cd Code/Main/ && python flaskServey.py`
3. In a new terminal window, begin executing CURL commands to Read and Write data from and to the MongoDb instance.

## Learning Experiences

## DEMO CURL Commands

#### GET Commands with Filter Parameters:
```sh
1. curl 'http://127.0.0.1:5000/.json'
2. curl -X GET 'http://127.0.0.1:5000/.json'
3. curl -X GET 'http://127.0.0.1:5000/.json?print=pretty'
4. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&print=pretty'
5. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$value"&print=pretty'
6. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102'
7. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106'
8. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToFirst=2'
9. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToLast=2'
10. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$key"&print=pretty'
11. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$key"&limitToFirst=2&print=pretty'
12. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$value"&print=pretty'
13. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$value"&startAt=30&print=pretty'
14. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$value"&limitToFirst=2&startAt=30&print=pretty'
15. curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$key"&print=pretty'
```

#### Error Handling:
1. curl -X GET 'http://127.0.0.1:5000/users.json?equalTo=age'
2. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&limitToFirst=2&limitToLast=3'
3. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102&startAt=13'
4. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="name"'

#### Write Data with PUT, POST, PATCH and DELETE:
1. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"109": {"name": "Miles", "age": 36}}
2. curl -X PUT 'http://127.0.0.1:5000/users/110.json' -d '{"name": "Jenny", "age": 20}'
3. curl -X PATCH 'http://127.0.0.1:5000/users/102.json' -d '{"name": "Amanda", "location": "California"}'
4. curl -X DELETE 'http://127.0.0.1:5000/users/110.json'


































Upload a single file from a specific local director to a specifc directory on EC2:
`scp -i "dsci551-2023.pem" "/Users/toddgavin/Desktop/USC_Classes/DSCI551 - Data Management/GitHub/DSCI551-FirebaseEmulator/code/mongoDBconnect.py" ubuntu@ec2-52-37-233-74.us-west-2.compute.amazonaws.com:/home/ubuntu/FirebaseEmulator/`

## Connect to MongoDB on EC2 instance through shell:
1. Update `mongod.conf` file in directory /etc/. 
    - Run command: `sudo nano mongod.conf`
    - Change bindIP to `bindIp: 127.0.0.1;52.37.233.74;10.26.175.35`

Refer to this Piazza Post: https://piazza.com/class/lcnpg1xru9v6jg/post/413 

## Trouble Shooting connecting to MongoDB Atlas using PyMongo Pyhton Driver
Refer to this Piazza Post: https://piazza.com/class/lcnpg1xru9v6jg/post/649
- Change the user access from `readAndWriteOnly` to `admin`
- Really ensure that you whitelist the correct IP adresses:
    - You can whitelist all IPs using `0.0.0.0/0`
- Must be using python env `Python 3.10.6`

### Connecting to MongoDB Database

### RESTful API
- Implement RESTful Server using Flask App

### Operational Functions:
1. PUT: A function to update an existing document in the database. 
3. GET: A function to retrieve a document from the database. 
3. POST: A function to create a new document in the database. 
4. PATCH: A function to partially update a document in the database. 
5. DELETE: A function to delete a document from the database. 
6. Filtering functions: Functions to filter documents based on the query parameters provided in the URL, such a:
    - orderBy
    - limitToFirst/Last
    - equalTo
    - startAt/endAt

### Document Indexing


### Command Line Interface

### DEMO TESTING COMMANDS
1. curl -X GET 'http://127.0.0.1:5000/.json'
    - curl 'http://127.0.0.1:5000/.json'

curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$value"&print=pretty'
curl -X GET 'http://127.0.0.1:5000/users/102.json?orderBy="$key"&print=pretty'

6. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"'
   curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102'
7. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106'
8. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToFirst=2'
9. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&startAt=102&endAt=106&limitToLast=2'

Errors:
curl -X GET 'http://127.0.0.1:5000/users.json?equalTo=age'
curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&limitToFirst=2&limitToLast=3'
curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102&startAt=13'
curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="name"'

WRITE DATA V2:
2. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"109": {"name": "Miles", "age": 36}}'
3. curl -X PUT 'http://127.0.0.1:5000/users/110.json' -d '{"name": "Jenny", "age": 20}'
4. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"country": "USA"}'
5. curl -X PATCH 'http://127.0.0.1:5000/users/102.json' -d '{"name": "Amanda", "location": "California"}'
6. curl -X DELETE 'http://127.0.0.1:5000/users/110.json'

NEED TO INCLUDE print=pretty

---------------------------------------------

WRITE DATA V1:
2. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"108": {"name": "Johnny", "age": 33}}'
3. curl -X PUT 'http://127.0.0.1:5000/users/106.json' -d '{"name": "Grace", "age": 42}'
4. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"weatherType": "Sunny"}'
5. curl -X PATCH 'http://127.0.0.1:5000/users/102.json' -d '{"name": "Jack", "height": 58}'

