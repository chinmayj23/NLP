from __future__ import division
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from tweets import twitter_analyze
import LA
import pdb
import chatterbot
app = Flask(__name__)

      
chatbot = ChatBot("Michael Blurry", storage_adapter="chatterbot.storage.SQLStorageAdapter",logic_adapters=[
         {
            'import_path': 'LA.MyLogicAdapter'
        },
         {
             'import_path':'chatterbot.logic.SpecificResponseAdapter',
             'input_text':'What can you do?',
             'output_text':'I can tell you the market sentiment for a particular stock'
        }
    ])

#trainer = ChatterBotCorpusTrainer(english_bot)
#trainer.train("chatterbot.corpus.english")

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/get")
def get_bot_response():
      
        input_text = request.args.get('msg')   
        response = str(chatbot.get_response(input_text))
        return response


if __name__ == "__main__":
    app.run()
