# Backend - Trivia API
This is a Trivia API that allows user to create, read and delete qtrivia questions. Categories are preset and new ones are not allowed in this version.
API return json objects.

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
`DELETE '/api/v1.0/questions/<int:question_id>'`
- Delete method that queries database for a question id. If id the query does not return a question due to question not found a 404 error is thrown.
- Response includes a success, status_code, list og paginated questions and the total number of questions
- Request Arguments: the id of question is part of the request object

```json
{
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
  "total_questions": 21
}

"GET '/api/v1.0/questions'"
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a dictionary of questions in which the keys are question, answer, category, difficulty and the values are Strings for all keys except difficulty which is an Integer
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs. The response also include current category selected, questions, status code, success code and total number of questions.
Example below:

``` json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
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
  "total_questions": 22
}

"POST '/api/v1.0/questions'"
- method that creates a new question of a new search based on serarchTerm. 
- Request: Object sends over question, answer, category, difficulty and searchTerm.
- the searchTerm is used to query database. 
- the rest of the request is used to create a new question
- Returns: An json object with a list of questions, the total number of questions and the success code.
NOTE: The total number of questions for search result will be the total number of questions that contains searchTerm whereas the total number of questions for new question will be all the questions.
Example below:

``` json
searchTerm response:
{
  "questions": [
    {
      "answer": "Mercury",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "What is the nearest planet to the sun?"
    }
  ],
  "success": true,
  "total_questions": 1 
}
new_question response:
{
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
  "total_questions": 22
}

"GET '/api/v1.0/questions/<int:category_id>/questions'"
- Fetches categories and questions filtered by category
-Response object shows success status, length of questions in category and the questions in category.
-This list is paginated with total number of questions in particular category
Example below:
``` json
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ], 
  "success": true, 
  "total_questions": 1
}

"POST '/api/v1.0/quizzes'"
-Post method with request object that contains quiz category and a list of ids for previous question that have already been used
- response returns success and the next question
``` json
request object example:
{
  "quiz_category":{"type":"Science","id":"1"},"previous_questions":[21]
  }
response object example:
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
