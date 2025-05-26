from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages=[message.to_dict() for message in Message.query.all()]

    response = make_response(
        messages,
        200
    )
    return response
@app.route('/messages/<int:id>')
def messages_by_id(id):
    message=Message.query.filter(Message.id==id).first()

    message_dict=message.to_dict()

    response=make_response(
        message_dict,
        200
    )
    return response
@app.route('/messages', methods=['POST'])
def create_new_message():
    data = request.get_json()

    if not data or 'body' not in data or 'username' not in data:
        return make_response({'error': 'Missing required fields'}, 400)

    new_message=Message(
        body= data['body'],
        username=data['username'])
    
    db.session.add(new_message)
    db.session.commit()

    return make_response(new_message.to_dict(), 201)
         
@app.route('/messages/<int:id>', methods=["PATCH"])
def update_message(id):
    message= Message.query.filter(Message.id==id).first()
    if not message:
        return make_response({'error': 'Message not found'}, 404)
    data=request.get_json()
    print("PATCH received JSON:", data)

    if 'body' in data:
        message.body=data['body']

        db.session.commit()

        response=make_response(
            message.to_dict(),
            200
        )
        return response

@app.route('/messages/<int:id>', methods=["DELETE"])
def delete(id):
    message = Message.query.filter(Message.id == id).first()
    if not message:
        return make_response({'error': 'Message not found'}, 404)
    db.session.delete(message)
    db.session.commit()

    response = make_response({}, 204)
    return response


if __name__ == '__main__':
    app.run(port=5555)
