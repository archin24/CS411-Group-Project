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

@app.route("/results.html")
def result():
    return(render_template('results.html'))

@app.route("/events.html")
def events():
	genre = input('genre:')
	city = input('city:')
	subgenreCode = getGenreCode(genre)
	response = getMusicEvents(city, subgenreCode)
    return(render_template('events.html', response = response))

@app.route("/news.html")
def news():
    return(render_template('news.html'))

@app.route("/contact.html")
def contact():
    return(render_template('contact.html'))

@app.route("/about.html")
def about():
    return(render_template('about.html'))





# The search bar
@app.route("/search", methods=['POST'])
def Test():

    artist = input('artist name:')
    #artist = 'coldplay'
    artist_id = checkCache(artist)

    url = "https://api.spotify.com/v1/artists/" + artist_id

    headers = {
        'Authorization': "Bearer BQDpbxVhgDTEkPgKmt10S-sfJ09ZlaNTWfjhutqWgpdiZSbRKSM8oXIMyYK60qjJLTJbuk_CwuSq9NOILmoc6BPRD_EFzqIVqeTWAiyc30UEH5At2CecrQmRP_TbSEajc150QVZ-2vaMNWFOdqkv5ptyUQ96_9c",
        'Cache-Control': "no-cache",
        'Postman-Token': "a6b84a57-f95f-49e8-b399-953f887328e4"
    }

    response = requests.request("GET", url, headers=headers)
    

    artist_info = response.json()


    return(render_template('results.html', artist_info = artist_info))
    #return(str(json.dumps(json_data, sort_keys=True, indent=4)))


# Checks the cache to see if the artist's id is already there. If not, makes API call and puts it in
def checkCache(artist):
    if collection.find_one({"artist": artist}) != None:
        return collection.find_one({"artist":artist})['id']
    else:
        # MAKE THE API CALL
        url = "https://api.spotify.com/v1/search"

        querystring = {"q":artist,"type":"artist"}

        headers = {
            'Authorization': "Bearer BQDpbxVhgDTEkPgKmt10S-sfJ09ZlaNTWfjhutqWgpdiZSbRKSM8oXIMyYK60qjJLTJbuk_CwuSq9NOILmoc6BPRD_EFzqIVqeTWAiyc30UEH5At2CecrQmRP_TbSEajc150QVZ-2vaMNWFOdqkv5ptyUQ96_9c",
            'Cache-Control': "no-cache",
            'Postman-Token': "ef420abf-6166-4c0d-ba3d-02306d888b81"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        

        json_data = response.json()
        artist_id = json_data["artists"]["items"][0]["id"]

        collection.insert_one({"artist": artist, "id": artist_id})
        #print(collection.find_one({"artist":artist})['id'])
        return collection.find_one({"artist":artist})['id']

def getGenreCode(genre):
    if genre =="Alternative":
        return "3001"
    if genre == "Blues & Jazz":
        return "3002"
    if genre == "Classical":
        return "3003"
    if genre == "Country":
        return "3004"
    if genre == "Cultural":
        return "3005"
    if genre == "EDM / Electronic":
        return "3006"
    if genre == "Folk":
        return "3007"
    if genre == "Hip Hop / Rap":
        return "3008"
    if genre == "Indie":
        return "3009"
    if genre == "Latin":
        return "3010"
    if genre == "Metal":
        return "3011"
    if genre == "Opera":
        return "3012"
    if genre =="Pop":
        return "3013"
    if genre =="R&B":
        return "3014"
    if genre == "Reggae":
        return "3015"
    if genre == "Religious/Spiritual":
        return "3016"
    if genre == "Rock":
        return "3017"
    if genre == "Top 40":
        return "3018"
    if genre =="Other":
        return "3019"
    else:
        print("No Genre given")

def getMusicEvents(city, subgenreCode):
    response = requests.get(

        "https://www.eventbriteapi.com/v3/events/search/?location.address=" + city +  "&categories=103&subcategories="+ subgenreCode + "&token=Y7BYBBACTDQLL3MR6XBX",
        headers = {
            "Authorization": "Bearer Y7BYBBACTDQLL3MR6XBX",
         },
        verify = True,  # Verify SSL certificate
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)



