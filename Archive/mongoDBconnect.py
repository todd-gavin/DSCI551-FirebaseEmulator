from pymongo import MongoClient

# Replace the IP address with your EC2 instance's public IP address
client = MongoClient('mongodb://52.37.233.74:27017/')

print("Client Connected")

# EC2 = 52.37.233.74

# To determine the IP of your EC2, run this command in your EC2 terminal: curl http://checkip.amazonaws.com

db = client['mydb_test']

print("Ran DB")

# Insert a document into a collection named 'mycollection'
mycollection = db['mycollection']
mydocument = {'name': 'John', 'age': 30}

print("Create Data")

result = mycollection.insert_one(mydocument)

print("Inserted Data")