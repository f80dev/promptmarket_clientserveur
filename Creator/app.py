

from flask import Flask
from Elrond import Elrond


app = Flask(__name__)


@app.route('/')
def prompt_list():  # put application's code here
    net=Elrond()
    t=net.create_transaction()

if __name__ == '__main__':
    app.run()
