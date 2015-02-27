#### SETUP ####
## Import statements: they're pretty standard with Python. They allow us to use code from Flask
## and other packages that aren't directly in this file.
import datetime
from flask import Flask, render_template, request, url_for, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config.from_object('config')        ## Configuration file.
db = SQLAlchemy(app)                    ## Attaches SQLAlchemy to our database.

###############
#### VIEWS ####

@app.route('/') ## @app.route tells you what web address to request when viewing this page
def index():    ## This is all it takes to render a page with no info from the database - a "static" page.
	return render_template('index.html')


@app.route('/', methods=['POST'])   ## In this case, we use a POST request to send data from the template to the server.
def hello():                        ## This method CREATES a new message to be put in the database, so we can display it later.
    text = request.form['text']
    latitude = request.form['latitude']     ## Each of these are part of the form we submit on the front page.
    longitude = request.form['longitude']   ## Latitude and longitude are found by an HTML5 plugin - we might talk about that later.
    timestamp = datetime.datetime.utcnow()

    latitude = float(latitude)
    longitude = float(longitude)
    
    message = Message(text = text, latitude = latitude, longitude = longitude, timestamp = timestamp)   #//COMMENT OUT
            ## Create an instance of the model with each of the arguments:
            ## text, latitude, longitude, and timestamp.
    db.session.add(message) #//COMMENT OUT
            ## In this database session, add the message to the database.
    db.session.commit() #//COMMENT OUT
            ## Now save (commit - just like Git!) the session to the database.
    return render_template('index.html') #//COMMENT OUT
            ## Then render the template you want to show - in this case, we just want to go back to index.html.


@app.route('/messages/<latitude>/<longitude>')
def ajax(latitude, longitude):
    ## messages = Message.query.all()   ## Uncomment this line for testing purposes. Recomment in production.
    minLat = float(latitude) - .05      ## SUPER HACKY GEOLOCATION SYSTEM WOOOOOO
    maxLat = float(latitude) + .05      ## Just so you know, 1/60 of a degree (or .005) is ~ 1 mile, so that times three is .05 degrees.
    minLong = float(longitude) - .05    ## That gives us a box of around 36 square miles (3 miles N/S/E/W from your location).
    maxLong = float(longitude) + .05    ## END OF SUPER HACKY GEOLOCATION SYSTEM

    messages = Message.query.filter(Message.latitude > minLat, Message.latitude < maxLat, Message.longitude > minLong, Message.longitude < maxLong)
        ## The above statement is a little hacky, so let me explain:
        ## the query.filter() function allows you to filter what you want back from the database.
        ## In this case, we want our latitude and longitude to be between our allowable minimums and maximums.
    messages = messages.order_by(Message.timestamp.desc()) #//COMMENT OUT
        ## Default ordering of queries is a little strange: let's flip it around so the newest submission is seen at the top.
        ## We want to order the above messages in descending order by timestamp.
    return render_template('messages.html', messages = messages) #//COMMENT OUT
        ## Render the template you want to show - this time, we want messages.html, and we need to pass messages as an argument as well.

################
#### MODELS ####

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(140)) #//COMMENT OUT     ## Create a column in the database of type String, with a max length of 140 characters for our text.
    latitude = db.Column(db.Float) #//COMMENT OUT       ## Create a column in the database of type Float for our latitude.
    longitude = db.Column(db.Float) #//COMMENT OUT      ## Create a column in the database of type Float for our longitude.
    timestamp = db.Column(db.DateTime) #//COMMENT OUT   ## Create a column in the database of type DateTime for the timestamp.

    def __repr__(self):
        return '<Post %r>' % (self.body)

################

if __name__ == '__main__':
    app.run(debug = True)   ## debug = True will give you a stack trace if an error occurs. You will want to remove this
                            ## statement if you ever want to push this to a production server.
