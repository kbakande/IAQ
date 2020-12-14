# Healthy-Air -- An Indoor Air Quality Monitoring Solution
Healthy-Air is an innovative solution that is developed to significantly effect attitudinal changes and alter the behaviour of the general populace towards indoor air quality. Healthy-Air achieves its objectives through AI-based analytics and intuitive visualisation, that are designed to persuade the users to take action towards improving poor indoor air quality. The healthy-Air app is deployed on Heroku and live at [Healthy-Air](https://healthy-air.herokuapp.com/). 

The code follows [PEP 8 style guide](https://pep8.org/).

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.  

## Web Interface Launch
From with the `frontend` directory, launch the `index.html` file. This shows the current status of the healthy-air platform.

### API Reference

### Getting Started

* BASE URL: The healthy-air is hosted on Heroku.
* This version of the application does not require authentication

### Error Handling

Errors are returned as JSON objects in the following formats:

```json
{ 
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return two types of errors when a request fails:

* 404: Request Not Found
* 422: Unprocessable

### Endpoints


```bash
curl https://healthy-air.herokuapp.com/forecast -H 'Content-Type: application/json' -X POST -d '{"sensor": 0, "pollutant": "Temperature", "reqDate": "2020-12-03"}'
```

GET /categories
* General
    - Returns an object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    - Request Arguments: Results are paginated in groups of 10. Include an optional request argument to specify page number, starting from 1
* Sample: 

```bash
 curl 127.0.0.1:5000/categories 
 ```

```json
{
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "success":true
}
```


DELETE /questions/{question_id}
* General
    - Deletes the question of the given id if it exists. Returns the id of the deleted question, success value, total questions and questions list 
      based on the current page number to update the frontend.

* Sample: 

```bash
  curl -X DELETE http://127.0.0.1:5000/questions/16?page=2
 ```

```json
{
  "deleted_id": "13",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```


POST /forecast
* General
    - Requests for the 3-day forecast. Returns the i

* Sample: 

```bash
  curl -X POST -H "Content-Type: application/json"  -d '{"sensor": 0, "pollutant": "Temperature", "reqDate": "2020-12-03"}' http://healthy-air.heroku.com
 ```

```json
{
 
}
```

## Testing
To run the tests, run


### Terms of Use

