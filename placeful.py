from flask import Flask, render_template, request, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug = True)

