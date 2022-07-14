#importing all relevant packages
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

#define the number of questions to be displayed on a page
QUESTIONS_PER_PAGE = 10
list_rand_num = []
#defining paginated function that will setup number of pages
def paginate_lists(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    items = [item.format() for item in selection] 
    current_lists = items[start:end]

    return current_lists

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Setting up CORS to allow '*' for origins. 
    """
    CORS(app,resources={r"/api/*": {"origins": "*"}})

    """
    After_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    Endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        #body = request.get_json()
        category_list = Category.query.all()
        categories ={}
        for category in category_list:
            categories[category.format()["id"]] = category.format()["type"]
            

        #print(categories,file=sys.stdout)
        if categories is None:
            abort(404)
        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(categories)
        })
        

    """
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.
    """
    @app.route("/questions")
    def retrieve_questions():
        category_list = Category.query.all()
        categories ={}
        for category in category_list:
            categories[category.format()["id"]] = category.format()["type"]
            
    
        questions_list = Question.query.all()
        questions = paginate_lists(request,questions_list)

        
        if len(questions) ==0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(questions_list),
            "current_category": None,
            "categories": categories
        })

    """
    Endpoint to DELETE question using a question ID.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        print(question_id,file=sys.stdout)
        try:
            question = Question.query.get(question_id)
            print(question,file=sys.stdout)
            if question is None:
                 abort(404)

            question.delete()
            question_list = Question.query.all()
            #print(question_list,file=sys.stdout)
            questions = paginate_lists(request, question_list)
            return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(question_list)
        })
            
        except:
            print(sys.exc_info)
            abort(422)
    
    """
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    """
    @app.route("/questions", methods=["POST"])
    def new_question():
        body = request.get_json()
        #create variables that for question, answer, etc
        new_question = body.get("question", None)
        new_answer = body.get("answer",None)
        new_category = body.get("category")
        new_difficulty = body.get("difficulty")
        search = body.get("searchTerm",None)
        try:
            # catch search request and return json for searchterm
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
                current_questions = paginate_lists(request, selection)
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    }
                )
            # catch new question request and save to database
            elif new_question:
                question = Question(
                    question=new_question, 
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                    )
                question.insert()
                question_list = Question.query.all()
                questions = paginate_lists(request, question_list)
                return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(question_list)
            })
        except:
            abort(422)

    """
    GET endpoint to get questions based on category.
    """
    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def retrieve_questions_by_category(category_id):
        # query to get the list filtered by category   
        question_list = Question.query.filter(Question.category==category_id).all()
        #create a paginated list 
        questions = paginate_lists(request, question_list)
        #print(questions,file=sys.stdout)

        if questions is None:
             abort(404)
        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(question_list)
        })
    """
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route("/quizzes",methods=["POST"])
    def retrieve_quiz():
        #collecting data from rquest
        body = request.get_json()
        current_category = body.get("quiz_category")
        previous_question =body.get("previous_questions")
        print(f"question: {current_category}, previous: {previous_question}",file=sys.stdout)
        if current_category is None and len(previous_question) ==0:
            abort(404)
        #getting the total number of question filtered by category
        total_questions = Question.query.filter(Question.category==current_category["id"]).all()
        #print(len(total_questions),file=sys.stdout)
        #print(len(previous_question),file=sys.stdout)
        #checkinhg if we have gone throught the entire list of questions
        if len(previous_question) == len(total_questions):
            return jsonify({
                'success': True,
                'done':"You have viewed every question"
            })
        #query to get questions that filter out questions used prior
        questions = Question.query.filter(Question.category==current_category["id"]).filter(Question.id.notin_(previous_question)).all()
        next_question = random.choice(questions).format()
        
        

        return jsonify({
            'success':True,
            'question':next_question
        })
  

    """
    Error handlers for all expected errors.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    return app

