# DSCI551-FirebaseEmulator

Upload a single file from a specific local director to a specifc directory on EC2:
`scp -i "dsci551-2023.pem" "/Users/toddgavin/Desktop/USC_Classes/DSCI551 - Data Management/GitHub/DSCI551-FirebaseEmulator/code/mongoDBconnect.py" ubuntu@ec2-52-37-233-74.us-west-2.compute.amazonaws.com:/home/ubuntu/FirebaseEmulator/`

## Connect to MongoDB on EC2 instance through shell:
1. Update `mongod.conf` file in directory /etc/. 
    - Run command: `sudo nano mongod.conf`
    - Change bindIP to `bindIp: 127.0.0.1;52.37.233.74;10.26.175.35`

Refer to this Piazza Post: https://piazza.com/class/lcnpg1xru9v6jg/post/413 

## Trouble Shooting onnecting to MongoDB Atlas using PyMongo Pyhton Driver
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

