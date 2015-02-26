import datetime
from flask import Flask, render_template, request, url_for, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)

#### VIEWS.PY ####

@app.route('/') ## @app.route tells you what web address to request when viewing this page
def index():    ## This is all it takes to render a page with no info from the database - a "static" page.
	return render_template('index.html') #//COMMENT OUT


@app.route('/', methods=['POST']) ## In this case, we use a POST request to send data from the template to the server.
def hello():    ## This method CREATES a new message to be put in the database, so we can display it later.
    text = request.form['text']
    latitude = request.form['latitude']     ## Each of these are part of the form we submit on the front page.
    longitude = request.form['longitude']   ## Latitude and longitude are found by an HTML5 plugin - we might talk about that later.
    timestamp = datetime.datetime.utcnow()

    latitude = float(latitude)
    longitude = float(longitude)
    
    message = Message(text = text, latitude = latitude, longitude = longitude, timestamp = timestamp) #//COMMENT OUT
    db.session.add(message) #//COMMENT OUT
    db.session.commit() #//COMMENT OUT
    # save it to db
    return render_template('index.html') #//COMMENT OUT

@app.route('/messages/<latitude>/<longitude>')
def ajax(latitude, longitude):
    # messages = Message.query.all()
    minLat = float(latitude) - .05
    maxLat = float(latitude) + .05
    minLong = float(longitude) - .05    ## Well, I hope you weren't 
    maxLong = float(longitude) + .05    ## looking for a Tinder success story.
    messages = Message.query.filter(Message.latitude > minLat, Message.latitude < maxLat, Message.longitude > minLong, Message.longitude < maxLong) #//COMMENT OUT
    messages = messages.order_by(Message.timestamp.desc()) #//COMMENT OUT

    return render_template('messages.html', messages = messages) #//COMMENT OUT

# Run the app :)

###################
#### MODELS.PY ####

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(140)) #//COMMENT OUT
    latitude = db.Column(db.Float) #//COMMENT OUT
    longitude = db.Column(db.Float) #//COMMENT OUT
    timestamp = db.Column(db.DateTime) #//COMMENT OUT

    def __repr__(self):
        return '<Post %r>' % (self.body)


###################

if __name__ == '__main__':
    app.run(debug = True)

