import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','Webster1981qawsed', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"question":"how far is the moon from the earth?" ,"answer":"238,900 mi","category":"1","difficulty":"3"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    """
    TEST: Checking to see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def test_get_catgories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    """
    TEST: Checking requests that are beyond the number of pages that are available.
    404 Error should return if page requested is beyond the current number of pages
    """
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    """
    TEST: returns paginated page of questions with 10 questions per page
    """
    def test_get_questions_paginated(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    def test_delete_question(self):
        res = self.client().delete("/questions/59")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
       

    """
    TEST: This will test if the question does not exist when trying to delete the question
    """
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    """
    TEST: Submit a new question,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    def test_create_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))

    

    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """   
    def test_search_question(self):
        res =self.client().post("/questions", json={"searchTerm":"planet"})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))

    
    """ 
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    def test_get_question_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    def test_post_play_quiz(self):
        res = self.client().post("/quizzes", json={"quiz_category":{"type": "History", "id":"4"},"previous_questions":["5"]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()