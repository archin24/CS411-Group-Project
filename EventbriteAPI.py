import requests


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

def Test():
    testCity = "Boston"
    testGenre = "Rock"
    testGenreCode = getGenreCode(testGenre)
    testResponse = getMusicEvents(testCity, testGenreCode)
    print(testResponse.json())

Test()