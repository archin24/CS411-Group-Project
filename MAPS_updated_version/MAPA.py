import requests
from flask import Flask, request, render_template, redirect, g
import json
import pymongo
from pymongo import MongoClient
import urllib
import base64

app = Flask(__name__)

client = MongoClient()
db = client.cache
collection = db.artist_ids
#collection.delete_many({})

CLIENT_ID = "77e6d4e10ead432ab6f95f1e51fb0bc5"
CLIENT_SECRET = "2234eeb3659d43919aedd1d64c60f709"

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)

auth_query_parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        #"scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
}

@app.route("/")
def home():
    return(render_template('index.html'))

@app.route("/index.html")
def index():
    return(render_template('index.html'))

@app.route("/login")
def login():

    url = "https://accounts.spotify.com/authorize"

    response = requests.request("GET", url)

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(url, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():

    url = "https://accounts.spotify.com/api/token"

    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    data_str = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    data_bytes = data_str.encode("utf-8")
    base64encoded = base64.b64encode(data_bytes)
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(url, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    #access_token = response_data["access_token"]
    #refresh_token = response_data["refresh_token"]
    #token_type = response_data["token_type"]
    #expires_in = response_data["expires_in"]

    #authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    #return render_template("index.html")
    return(str(json.dumps(response_data, sort_keys=True, indent=4)))

@app.route("/results1.html")
def result():
    return(render_template('results1.html', artist_info))

@app.route("/events.html")
def events():
    return(render_template('events.html'))

@app.route("/news.html")
def news():
    return(render_template('news.html'))

@app.route("/contact.html")
def contact():
    return(render_template('contact.html', user))

@app.route("/about.html")
def about():
    return(render_template('about.html'))





# The search bar
@app.route("/search", methods=['POST'])
def Test():

    #artist = input('artist name:')
    artist = 'coldplay'
    artist_id = checkCache(artist)

    url = "https://api.spotify.com/v1/artists/" + artist_id

    headers = {
        'Authorization': "Bearer BQCtuh-jlkmD5y_GyqXeWuGcjCGfAvZTNxMd8RNAfIe0F-hyepgpyrCIlieZ5nMiwGqX57prTlstHgoF6plDoexWgDeLIbcuwxd7yGDXxEpckUJihxmn-MfI2FuQrY5w0Kx_IFFKcZFz",
        'Cache-Control': "no-cache",
        'Postman-Token': "a6b84a57-f95f-49e8-b399-953f887328e4"
    }

    response = requests.request("GET", url, headers=headers)
    

    json_data = response.json()


#    return(render_template('index.html'))
    return(str(json.dumps(json_data, sort_keys=True, indent=4)))


# Checks the cache to see if the artist's id is already there. If not, makes API call and puts it in
def checkCache(artist):
    if collection.find_one({"artist": artist}) != None:
        return collection.find_one({"artist":artist})['id']
    else:
        # MAKE THE API CALL
        url = "https://api.spotify.com/v1/search"

        querystring = {"q":artist,"type":"artist"}

        headers = {
            'Authorization': "Bearer BQCtuh-jlkmD5y_GyqXeWuGcjCGfAvZTNxMd8RNAfIe0F-hyepgpyrCIlieZ5nMiwGqX57prTlstHgoF6plDoexWgDeLIbcuwxd7yGDXxEpckUJihxmn-MfI2FuQrY5w0Kx_IFFKcZFz",
            'Cache-Control': "no-cache",
            'Postman-Token': "ef420abf-6166-4c0d-ba3d-02306d888b81"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        

        json_data = response.json()
        artist_id = json_data["artists"]["items"][0]["id"]

        collection.insert_one({"artist": artist, "id": artist_id})
        #print(collection.find_one({"artist":artist})['id'])
        return collection.find_one({"artist":artist})['id']



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
'''
