from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from dataextraction import UrlExtract,readlogs
import requests
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
#Documentation for Home Page
tasks = [
    {
        'url':'/',
        'Method':'GET',
        'Description':'returns the API documentation'
    },
    {
        'url':'/knowledge-base',
        'Method':'POST',
        'data':'Json format of features',
        'Description':'create knowledge based using a query'
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found','status':404}), 404)
   
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal server Error','status':500}), 500)
   
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request Error, Please give valid input', 'status':400, }), 400)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method not allowed , this URL takes POST method ','status':405}), 405)

def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'error': message, 
    })
    response.status_code = status_code
    return response
class bitWise(Resource):
   #Index of API
    @app.route("/")
    def index():
        return jsonify({'docs':tasks})

    #API to get model output
    @app.route("/knowledge-base",methods=["POST"])
    def getproposedpath():

        data = request.get_json(force=True)
        query = data.get('query')
        lang = data.get('lang')
        content_type = data.get('content_type')
        search_engine = data.get('search_engine')
        filename = data.get('filename')
        result = UrlExtract(query,lang,content_type,search_engine,filename)
        output= result.url_collection()
        return jsonify(output)

    @app.route("/logs")
    def logs():
        return jsonify(readlogs())

        # Define default parameters and their respective datatype in datamap() function before running verficiation code below.
        # dataparams, dtype, dataparams_main, dtype_main = datamap()
        # ver = verification(data, dataparams, dtype, dataparams_main, dtype_main)
        # if ver != '0':
        #     return ver

        # points = quiz_details['points']
        # total_points = quiz_details['total_points']
        # topics = quiz_details['topics']
        # val = validation('points', points, ulimit=total_points)
        # if val != '0':
        #     return val

        # previous_path = dataextraction
        # quiz_details['proposed_path'] = path_change

        # result = {"action": action, "user_id" : user_id, "course_id" : course_id, "quiz_details" : quiz_details, "previous_path" : previous_path}

        # return jsonify(previous_path)

if __name__ == "__main__":
    app.run(debug=True)

