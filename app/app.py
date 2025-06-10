from flask import Flask, jsonify, request, abort, Response
from flask_cors import CORS
from Assistant import Assistant
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Authorization", "Content-Type"]}})

API_KEY = 'your-api-key'
CHATGPT_API_KEY = 'your-api-key'
ASSISTANT_ID = 'your-assistant-id'
VECTOR_STORE_ID = 'your-vector-store-id'

# Assistant oluştur
assistant = Assistant(CHATGPT_API_KEY, ASSISTANT_ID, VECTOR_STORE_ID)

def check_api_key():
    api_key = request.headers.get('Authorization')
    if api_key and api_key.startswith('Bearer '):
        api_key = api_key.split(' ')[1]
    if api_key != API_KEY:
        abort(401)  # Yetkisiz

@app.route('/api', methods=["GET"])
def home():
    return "<h1>Assistant is Working!</h1>"

@app.route('/api/assistants', methods=['GET'])
def get_assistants():
    check_api_key()
    
    assistants_data = assistant.list_assistants().data

    assistants = []
    for asst in assistants_data:
        assistants.append({
            "id": asst.id,
            "name": asst.name,
            "description": asst.description,
            "created_at": datetime.fromtimestamp(asst.created_at).isoformat(),  
            "model": asst.model
        })

    return jsonify(assistants)

@app.route('/api/assistants/<string:assistant_id>', methods=['GET'])
def get_byid_assistant(assistant_id):   
    check_api_key()
    assistant_data = assistant.get_assistant(assistant_id)

    assistant_detail = {
        "id": assistant_data.id,
        "name": assistant_data.name,
        "description": assistant_data.description,
        "created_at": datetime.fromtimestamp(assistant_data.created_at).isoformat(),  
        "model": assistant_data.model
    } 

    return jsonify(assistant_detail)    


@app.route('/api/assistants/threads', methods=['POST'])
def create_thread():
    check_api_key()
    thread = assistant.create_thread()
    return jsonify({
        "threadId": thread.id
    }), 201

@app.route('/api/assistants/files', methods=['GET'])
def get_documents():
    check_api_key()
    try:
        documents = assistant.get_documents()

        if documents is None:
            return jsonify({
                "success": False,
                "error": "No documents found"
            }), 404

        serialize_documents = []
        
        for document in documents:
            serialize_documents.append({
                "id": document.id,
                "created_at": document.created_at,
                "filename": document.filename,
                "object": document.object,
                "purpose": document.purpose,
                "status": document.status,
                "status_details": document.status_details
            })

        return jsonify({
            "success": True,
            "data": serialize_documents
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/assistants/files/<string:file_id>', methods=['GET'])
def get_byid_document(file_id):
    check_api_key()
    try:
        file_content, file_detail = assistant.get_byid_document(file_id)

        if file_detail is None:
            return jsonify({
                "success": False,
                "error": "No document found"
            }), 404

        # Dosya indirme
        response = Response(file_content.body)
        response.headers['Content-Disposition'] = f'attachment; filename={file_detail.filename}'
        response.headers['Content-Type'] = 'text/plain'

        return response

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/assistants/files', methods=['POST'])
def post_documents():
    check_api_key()
    try:
        files = request.files.getlist("file")
        fileIds = []

        for file in files:
            file_id = assistant.create_documents(file)
            fileIds.append(file_id)
  
        return jsonify({
            'success': True,
            "fileIds": fileIds
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assistants/files', methods=['DELETE'])
def delete_documents():
    check_api_key()
    try:
        fileId = request.json['fileId']
        assistant.delete_document(fileId)

        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"An error occurred: {e}"
        }), 500

@app.route('/api/assistants/chat/message', methods=['POST'])
def chat_message():
    check_api_key()
    
    # JSON verisinden mesajı al
    if not request.json or 'message' not in request.json or 'threadId' not in request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400)  # Kötü İstek (Bad Request)

    message = request.json['message']
    threadId = request.json['threadId']
    email = request.json['email']
    password = request.json['password']

    user = assistant.get_user(email, password)
    if not user:
        return jsonify({
            'success': False,
            'error': f"User not found!"
        }), 400
    
    try:
        assistant.send_message(message, threadId)
        run = assistant.run()
    except Exception as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': f"An error occurred: {e}"
        }), 500
    
    response = {}
    statusCode = 201 

    if run.status == 'completed': 
        messages = assistant.get_messages(threadId).to_dict()

        response = {
            "success": True,
            "message_received": messages["data"][0]
        }
    elif run.status == "incomplete": # Tamamlanmamış      
        messages = assistant.get_messages(threadId).to_dict()

        response = {
            "success": True,
            "message_received": messages["data"][0]
        }
    elif run.status == "failed":
        response = {
            "success": False,
            "error": {
                'code': run.last_error.code,
                "message": "{run.last_error.code}: {run.last_error.message}"
            }
        }
        print(f"{run.last_error.code}: {run.last_error.message}")
        statusCode = 400
        return jsonify(response), statusCode
    else:
        messages = assistant.get_messages(threadId).to_dict()

        response = {
            "success": True,
            "message_received": messages["data"][0]
        }
        print("RUN ERROR: ", run)
        statusCode = 200
    return jsonify(response), statusCode

@app.route('/api/assistants/chat/delete-message', methods=['POST'])
def delete_message():
    check_api_key()
    
    # JSON verisinden mesajı al
    if not request.json or 'messageId' not in request.json or 'threadId' not in request.json:
        abort(400)  # Kötü İstek (Bad Request)

    messageId = request.json['messageId']
    threadId = request.json['threadId']

    deleted_message = assistant.delete_message(messageId, threadId)
    response = {}

    if deleted_message.deleted: 
        messages = assistant.get_messages(threadId).to_dict()
        
        response = {
            "success": True,
            "message_received": messages["data"]
        }
    else:
        response = {
            "success": False,
            "error": {
                "message": "Mesaj silinemedi!"
            }
        }
        print(deleted_message)
    return jsonify(response), 201

@app.route('/api/assistants/chat/messages/<string:threadId>', methods=['GET'])
def get_messages(threadId):
    check_api_key()
    response = {}
    messages = assistant.get_messages(threadId).to_dict()

    response = {
        "success": True,
        "messages": messages["data"]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
