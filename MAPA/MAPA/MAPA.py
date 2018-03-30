
import requests
from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def Test():
	url = "https://api.spotify.com/v1/search"

	#artist = input('artist name:')
	artist = 'coldplay'
	querystring = {"q":artist,"type":"artist"}

	headers = {
    	'Authorization': "Bearer BQAVMT8JAvRM8qgpsByuUv4Q1Gx_ay_v-X4Ub0075wGCwgp7QzPuuN4wznDK-WzS3geG4Qh91v_ONkzgWBuasyxG2uYLoyBq9djJfNLPO3d6T0teUhl176S-I0fzueXSHhngCn3Vo6DM",
    	'Cache-Control': "no-cache",
    	'Postman-Token': "ef420abf-6166-4c0d-ba3d-02306d888b81"
    	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	json_data = response.json()
	print(json.dumps(json_data, sort_keys=True, indent=4))
	return(str(json.dumps(json_data, sort_keys=True, indent=4)))

if __name__ == '__main__':
    app.run(debug=True)

'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request
import requests

app = Flask(_name_)

@app.route('/temperature', methods=['POST'])
def temperature():
    zipcode = request.form['zip']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=b0e0bbe93793b39e76cc1b1a65e32369')
    json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    temp_f = round(((temp_k - 273.15) * 1.8 + 32),1)
    return render_template('temperature.html', temp=temp_f)

@app.route('/')
def index():
	return render_template('index.html')

if _name_ == '_main_':
    app.run(debug=True)


from flask import Flask, render_template, request
import requests
import spotipy

sp = spotipy.Spotify()

app = Flask(__name__)

@app.route('/')
def Test():

    #zipcode = request.form['zip']
    artists = input('artist:')
    r = requests.get('https://api.spotify.com/v1/artists/'+artists)
    json_object = r.json()
    ##temp_k = float(json_object['main']['temp'])
    ##temp_f = round(((temp_k - 273.15) * 1.8 + 32),1)
    return str(json_object)

if __name__ == '__main__':
    app.run(debug=True)


	artist = input('artist name:')
	url = 'https://api.spotify.com/v1/search?q='+artist+'&type=artist'

	json_data = requests.get(url).json()

	return str(json_data)
	#api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=86309392d65f39d0c7612bad97ac704c&q='
	#city = input("city name:")

	url = api_address + city

	json_data = requests.get(url).json()

	return str(json_data)


'''


#Use Postman
