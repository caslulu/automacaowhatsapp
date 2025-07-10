
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from conversation_service import ConversationFlow
from extensions import db
from model import Cliente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


conversation_flow = ConversationFlow()

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    phone_number = request.values.get('From', '')
    response = MessagingResponse()

    # processa a mensagem usando o ConversationFlow
    reply = conversation_flow.process_message(phone_number, incoming_msg)
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)