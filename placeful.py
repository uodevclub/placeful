import datetime
from flask import Flask, render_template, request, url_for, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)

#### VIEWS.PY ####

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def hello():
    message = request.form['message']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    # save it to db
    return render_template('index.html')

# Run the app :)

###################
#### MODELS.PY ####

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.body)


###################

if __name__ == '__main__':
    app.run(debug = True)

