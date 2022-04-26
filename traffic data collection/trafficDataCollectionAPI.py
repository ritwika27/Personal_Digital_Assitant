import requests

api_file = open("APIkey.txt", "r")
api_key = api_file.read()
api_file.close()

home = input("Enter a home address\n")

work = input("Enter a work address\n")

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + api_key)
# print(r.json())
time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]

print("Total travel time:", time)