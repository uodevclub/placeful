import datetime
from flask import Flask, render_template, request, url_for, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)

#### VIEWS.PY ####

@app.route('/')
def index():
	messages = Message.query.all()
	return render_template('index.html', messages = messages)


@app.route('/', methods=['POST'])
def hello():
    text = request.form['text']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    timestamp = datetime.datetime.utcnow()
    
    message = Message(text = text, latitude = latitude, longitude = longitude, timestamp = timestamp)
    db.session.add(message)
    db.session.commit()
    # save it to db
    return render_template('index.html')

@app.route('/messages/<latitude>/<longitude>')
def ajax(latitude, longitude):
    return render_template('messages.html')

    minLat = latitude - (1/20)
    maxLat = latitude + (1/20)
    minLong = longitude - (1/20)    ## Well, I hope you weren't 
    maxLong = longitude + (1/20)    ## looking for a Tinder success story.
    messages = Message.query.filter(minLat < latitude, maxLat > latitude, minLong < longitude, maxLong > longitude)

# Run the app :)

###################
#### MODELS.PY ####

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(140))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.body)


###################

if __name__ == '__main__':
    app.run(debug = True)

