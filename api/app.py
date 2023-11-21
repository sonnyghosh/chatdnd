import os
from flask import Flask, request, jsonify, redirect, render_template, url_for
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


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
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)