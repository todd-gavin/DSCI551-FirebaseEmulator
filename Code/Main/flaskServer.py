from mongoDB_driver import connectMongoDB, db_collection_document, get, put, post, patch, delete

from flask import Flask, request
import json

# Build flask app
app = Flask(__name__)

# Create MongoDB client
client = connectMongoDB()

# Establish the database, collection, and document that data will be read/written from/to
db, collection, documentFilter = db_collection_document(client, 'firebaseRealtimeDatabase', 'firebaseCollection', '643c926ac5712e741b10398a')

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
    print(f"Log: collection: {collection}, documentFilter:{documentFilter}")

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
    print(f"Request method: {request.method}")

    # curl -X GET 'http://127.0.0.1:5000/'
    # curl -X GET 'http://127.0.0.1:5000/users/'
    if request.method == 'GET' or request.method == '':
        # Extract filter parameters from URL
        filter_params = {
            'orderBy': request.args.get('orderBy'),
            'limitToFirst': request.args.get('limitToFirst') if request.args.get('limitToFirst') else None,
            'limitToLast': request.args.get('limitToLast') if request.args.get('limitToLast') else None,
            'equalTo': request.args.get('equalTo'),
            'startAt': request.args.get('startAt'),
            'endAt': request.args.get('endAt'), 
            'print': request.args.get('print')
        }

        print(f"Filter Params1: {filter_params}")

        # Remove None values from the dictionary
        filter_params = {k: v for k, v in filter_params.items() if v is not None}
        filter_params = {key: str(value) for key, value in filter_params.items()}
        filter_params = {k: v.replace('"', '') for k, v in filter_params.items()}

        printPrettyFlag = False
        if filter_params.get('print') == 'pretty':
            printPrettyFlag = True
            del filter_params['print']
            print("Log: Pretty print activated")

        print(f"Filter Params2: {filter_params}")

        get_result = get(collection, documentFilter, jsonPath, filter=filter_params if filter_params else None)
        
        print("Log: GET Executed")
        print(f"Log: get_result = {get_result}")

        if jsonPath == '':
            get_result = dict(get_result)
            del get_result["_id"]

        if printPrettyFlag == True:
            get_result = json.dumps(get_result, indent=4)
        else: 
            get_result = str(get_result)

        return f"{get_result}\n"
    
    # curl -X POST 'http://127.0.0.1:5000/users/' -d '{"106": {"name": "Amanda", "age": 22}}'
    elif request.method == 'POST':
        if data:
            post(collection, documentFilter, jsonPath, data)
            print(f'Log: POST request received with data: {data}')
        else:
            print('Log: POST request received without data')
        print("Log: POST Executed")
        return str(data) + '\n'
    
    # curl -X PUT 'http://127.0.0.1:5000/users/' -d '{"105": {"name": "Amanda", "age": 22}}' 
    elif request.method == 'PUT':
        if data:
            put(collection, documentFilter, jsonPath, data)
            print(f'Log: PUT request received with data: {data}')
        else:
            print('Log: PUT request received without data')
        print("Log: PUT Executed")
        return str(data) + '\n'
    
    # curl -X PATCH 'http://127.0.0.1:5000/users/105/' -d '{"age": 26}' 
    elif request.method == "PATCH":
        if data:
            patch(collection, documentFilter, jsonPath, data)
            print(f'Log: PATCH request received with data: {data}')
        else:
            print('Log: PATCH request received without data')
        print("Log: PATCH Executed")
        return str(data) + '\n'
    
    # curl -X DELETE 'http://127.0.0.1:5000/users/105/'
    elif request.method == 'DELETE':
        get_result = get(collection, documentFilter, jsonPath, filter=None)
        print(f"Log: get_result that is delete {get_result}")
        delete(collection, documentFilter, jsonPath)
        print("Log: DELETE Executed")
        return 'null\n'
    
    else:
        return 'Invalid request'

if __name__ == '__main__':

    app.run(port=5000)