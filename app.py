from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register_user():
    pass


@app.route('/login', methods=['POST'])
def register_user():
    pass


@app.route('/report', methods=['GET'])
def create_report():
    # TODO if user not loggeed in show an error

    # TODO acccess the db
    # TODO accesss measurements
    # render template.....
    pass


#@app.route('/create_group')

if __name__ == '__main__':
    app.run()
