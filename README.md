# Emulating Firebase's Realtime Database using Flask and MongoDB

## Purpose
The purpose of this project was to emulate a large data storage system such as Firebase's Realtime Database using alternate systems such as MongoDB's NoSQL databse and Python Flask for the RESTful server.

## File Structure
- The program code is stored inside the directory `Code/Main/`
- There are two python files that work together to emulate Firebase's Realtime Database using Flask and MongoDB:
    - `flaskServer.py`: This file establishes the RESTful server to be able to listen for and accept CURL commands with GET, POST, PUT, PATCH, and DELETE.
    - `mongoDB_driver.py`: This file reads and writes data from and to the MongoDB Atlas instance.

## Implementation and Architecture

### `flaskServer.py`
This Python code implements a RESTful API using the Flask framework that interacts with a MongoDB database to perform CRUD (Create, Read, Update, and Delete) operations. The architecture of the code can be described as follows:

1. Import necessary libraries and functions:
   - Import the necessary functions from the custom `mongoDB_driver` module, which manages the connection and interaction with the MongoDB database.
   - Import the `Flask` class and the `request` object from the `flask` module to create the web application and handle incoming requests.
   - Import the `json` module for processing JSON data.

2. Initialize the Flask application and create a MongoDB client:
   - Instantiate a Flask app object.
   - Connect to the MongoDB server using the `connectMongoDB` function and store the client object.
   - Set up the database, collection, and document filter for reading/writing data.

3. Pre-process incoming requests:
   - Use the `before_request` decorator to ensure the content-type of incoming POST, PATCH, and PUT requests is set to `'application/json'`.

4. Define the request handler function:
   - Create a single function, `handle_request`, to handle all incoming requests for the RESTful API.
   - Use the `route` decorator to define the default and custom routes, and specify the allowed HTTP methods (GET, POST, PUT, PATCH, DELETE).
   - Inside the function, parse the path parameters, extract the JSON path, and retrieve the data from the request.
   - Based on the HTTP method, execute the respective CRUD function:
      - GET: Retrieve data from the MongoDB database.
      - POST: Create new data in the MongoDB database.
      - PUT: Update the entire data object in the MongoDB database.
      - PATCH: Update specific fields of the data object in the MongoDB database.
      - DELETE: Remove data from the MongoDB database.

5. Run the Flask application:
   - Use the `app.run()` function to start the Flask web server, specifying the desired port number (5000).

### `mongoDB_driver.py`
This code provides an interface for connecting to a MongoDB server, as well as performing CRUD (Create, Read, Update, and Delete) operations on the data stored in the database. The code uses the `pymongo` library to interact with MongoDB and `certifi` library for secure SSL/TLS certificate handling. The architecture of this code is as follows:

1. Connection to MongoDB:
   - The `connectMongoDB` function is responsible for connecting to a MongoDB instance using a URI that includes the username, password, and other necessary information for authentication. The `certifi.where()` method is used to obtain the CA certificate needed for SSL/TLS communication. The `ping` command is used to check if the connection was successful.

2. Accessing a specific database, collection, and document:
   - The `db_collection_document` function takes the `client`, `db_name`, `collection_name`, and `objectId` as inputs and returns references to the database, collection, and a filter for the specified document.

3. Custom sorting:
   - The `custom_sort_key` function sorts the data according to the following order: numbers, letters, special characters, and data types (like dicts, lists, and tuples).

4. Filtering data:
   - The `helper_filter` function applies filtering operations based on the provided filter parameters. The function handles various cases like ordering by keys or values, equalTo, limitToFirst, limitToLast, startAt, and endAt, among others.

5. CRUD operations:
   - The code contains functions to perform CRUD operations on the MongoDB data:
        - `get`: Retrieves data from the collection based on the document filter, JSON path, and additional filter parameters. It uses the `helper_filter` function to apply the required filters.
        - `put`: Updates the data in the MongoDB collection by replacing the specified JSON path with the new data. The `helper_Update_PUT` function is used to create the update command.
        - `post`: Adds new data to the MongoDB collection, creating a new unique key if necessary. The `helper_Update_POST` function is used to create the update command.
        - `patch`: Updates the data at the specified JSON path, either overwriting the existing data or creating new data if it doesn't exist.
        - `delete`: Removes data at the specified JSON path from the MongoDB collection.

This code effectively implements a RESTful API to communicate with a MongoDB database using the Flask web framework. The API enables users to perform various CRUD operations using CURL on the data stored in the MongoDB database, allowing for flexible and efficient data management.

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
1. Data validation and error handling:
   - This project demonstrates the importance of validating input data and handling errors. For example, checking if `limitToFirst` and `limitToLast` are integers and ensuring that only one of them is specified. Proper error handling not only improves the code's reliability but also makes it easier to debug and maintain.
2. Code modularity and organization:
   - The project is divided into different functions that handle specific tasks such as connecting to the database, filtering data, and performing CRUD operations. This modular design enhances code readability, maintainability, and makes it easier to extend the codebase in the future.
3. Custom sorting:
   - Implementing a custom sort function (`custom_sort_key()`) allows the code to sort data by numbers, letters, special characters, and data types. This is an excellent example of how to create custom sorting logic tailored to specific project requirements.
4. Working with MongoDB:
   - The project offers an opportunity to learn how to work with MongoDB, a popular NoSQL database. This includes connecting to a MongoDB instance using pymongo, defining and working with databases and collections, and performing CRUD operations.
5. RESTful API design:
   - The project demonstrates a simple RESTful API design using GET, PUT, POST, PATCH, and DELETE methods. Learning how to design and implement RESTful APIs is crucial for building modern web applications and microservices.
6. Filtering data:
   - The project shows how to implement filtering logic, such as filtering based on `equalTo`, `startAt`, `endAt`, `limitToFirst`, and `limitToLast` parameters. This is a valuable learning experience as it shows how to parse and apply filtering logic on the server-side, which is a common requirement in many applications.
7. Managing nested data structures:
   - The project handles nested data structures (dictionaries and lists) and demonstrates how to update and manipulate them using helper functions like `helper_Update_PUT()` and `helper_Update_POST()`.
8. Code commenting and logging:
   - The project includes numerous comments and log statements that explain what the code is doing and provides insights into the flow of execution. This can be a useful learning experience for understanding the importance of properly documenting and logging code for future maintainability and collaboration.

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
```sh
1. curl -X GET 'http://127.0.0.1:5000/users.json?equalTo=age'
2. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&limitToFirst=2&limitToLast=3'
3. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="$key"&equalTo=102&startAt=13'
4. curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="name"'
```

#### Write Data with PUT, POST, PATCH and DELETE:
```sh
1. curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"109": {"name": "Miles", "age": 36}}'
2. curl -X PUT 'http://127.0.0.1:5000/users/110.json' -d '{"name": "Jenny", "age": 20}'
3. curl -X PATCH 'http://127.0.0.1:5000/users/102.json' -d '{"name": "Amanda", "location": "California"}'
4. curl -X DELETE 'http://127.0.0.1:5000/users/110.json'
```
