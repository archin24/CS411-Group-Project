import requests
from flask import Flask
from flask import request
from flask import render_template
import json
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.cache
collection = db.artist_ids
#collection.delete_many({})

@app.route("/")
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
        print(collection.find_one({"artist":artist})['id'])
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

