import os
from flask import Flask, request, jsonify, redirect, render_template, url_for
from flask_cors import CORS
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from aiapi import generateStoryResponse

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)
# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route("/api/time")
def time():
    now = datetime.now()
    return {"time" : now}

@app.route('/table')
def show_table():
    # Retrieve data from Firestore (replace 'your_collection_name' with the actual collection name)
    table_data = todo_ref.get()
    return render_template('table.html', table_data=table_data)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        try:
            id = request.form['id']
            title = request.form['title']
            todo_ref.document(id).set({'id': id, 'title': title})
            return redirect('/table')
        except Exception as e:
            return f"An Error Occurred: {e}"
    return render_template('add.html')

@app.route('/remove/<string:id>')
def remove_data(id):
    # Remove data from Firestore
    todo_ref.document(id).delete()
    return redirect('/table')

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return render_template('game.html')  # You need to create a corresponding HTML template.

    elif request.method == 'POST':
        user_input = request.form.get('user_input')  # Assuming a form field named 'user_input'
        context += '\n'+user_input
        # Pass the user input to your AI function
        ai_response = generateStoryResponse(user_input)
        
        # You can then pass the response to the template or format it as needed
        return render_template('game.html', result=ai_response)

    # Handle other HTTP methods if necessary
    else:
        return "Method not allowed"
    
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)