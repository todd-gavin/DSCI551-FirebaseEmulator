# TODO:
# 1/ Implement GET filter functions
# 1.5/ Handle GET without "GET" method provided
# 2/ Error handling for when request methods are incorrect, data is incorrect (needs to match Firebase)
# 3/ Record 10 min Demo Video and upload to Youtube publicly
# 4/ Complete Self Assessment Form
# 5/ Write out final report and ReadMe file

# https://piazza.com/class/lcnpg1xru9v6jg/post/678

# Need to handle this case fo data where its just a string
# curl -X PUT 'https://dsci551-v1-default-rtdb.firebaseio.com/users/104/name.json' -d '"david smith sr"'
# "david smith sr"

# Need to handle this case where there is `.json` at the ned of the jsonPath
# curl -X DELETE 'https://dsci551-v1-default-rtdb.firebaseio.com/users/104/gender.json'
# null

from mongoDB_driver import connectMongoDB, db_collection_document, get, put, post, patch, delete

from flask import Flask, request, jsonify

# Build flask app
app = Flask(__name__)

# Create MongoDB client
client = connectMongoDB()

# Establish the database, collection, and document that data will be read/written from/to
db, collection, documentFilter = db_collection_document(client, 'firebaseRealtimeDatabase', 'firebaseCollection', '643c926ac5712e741b10398a')
# print(f"db: {db}\ncollection: {collection}\ndocumentFilter:{documentFilter}")

# Set request content-type to application/json 
@app.before_request
def before_request():
    if request.method in ['POST', 'PATCH', 'PUT']:
        request.environ['CONTENT_TYPE'] = 'application/json'

# Request handler function
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def handle_request(path):

    # Acces global variables to connect to MongoDB
    global collection
    global documentFilter
    # print(f"Log:\ncollection: {collection}\n\ndocumentFilter:{documentFilter}\n\n")

    # Get the path paramters to define where to read/write data from/to
    path_params = path.split('/')
    path_params = [string for string in path_params if string != ""]
    print(f"Log: path_params = {path_params}")

    # Create the JSON path using the path paramaters
    if len(path_params) == 1:
        jsonPath = path_params[0]
    else:
        jsonPath = ".".join(path_params)
    jsonPath = jsonPath.replace(".json", "")
    print(f"Log: jsonPath = {jsonPath}") 

    # Get the data from the CURL command
    data = request.get_json()

    # Check the request method, execute respective function to sed request method

    # curl -X GET 'http://127.0.0.1:5000/'
    # curl -X GET 'http://127.0.0.1:5000/users/'
    if request.method == 'GET':
        get_result = get(collection, documentFilter, jsonPath, filter=None)[0]
        print("Log: GET Executed")
        print(f"Log: get_result = {get_result}")
        return str(get_result)
    
    # curl -X POST 'http://127.0.0.1:5000/users/' -d '{"106": {"name": "Amanda", "age": 22}}'
    elif request.method == 'POST':
        if data:
            post(collection, documentFilter, jsonPath, data)
            print(f'Log: POST request received with data: {data}')
        else:
            print('Log: POST request received without data')
        print("Log: POST Executed")
        return str(data) + '\nPOST request received'
    
    # curl -X PUT 'http://127.0.0.1:5000/users/' -d '{"105": {"name": "Amanda", "age": 22}}' 
    elif request.method == 'PUT':
        if data:
            put(collection, documentFilter, jsonPath, data)
            print(f'Log: PUT request received with data: {data}')
        else:
            print('Log: PUT request received without data')
        print("Log: PUT Executed")
        return str(data) + '\nPUT request received'
    
    # curl -X PATCH 'http://127.0.0.1:5000/users/105/' -d '{"age": 26}' 
    elif request.method == "PATCH":
        if data:
            patch(collection, documentFilter, jsonPath, data)
            print(f'Log: PATCH request received with data: {data}')
        else:
            print('Log: PATCH request received without data')
        print("Log: PATCH Executed")
        return str(data) + '\nPATCH request received'
    
    # curl -X DELETE 'http://127.0.0.1:5000/users/105/'
    elif request.method == 'DELETE':
        get_result = get(collection, documentFilter, jsonPath, filter=None)[0]
        print(f"Log: get_result that is delete {get_result}")
        delete(collection, documentFilter, jsonPath)
        print("Log: DELETE Executed")
        return 'null \nDELETE request received'
    
    else:
        return 'Invalid request'

if __name__ == '__main__':

    app.run(port=5000)