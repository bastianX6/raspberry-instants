import requests
import time

url = "https://us-central1-raspberry-instants.cloudfunctions.net/botonera/song/add"

jsonBody = {
	"songName": "",
	"songCode": "",
	"description": "",
	"public": False
}

for i in range(10):
    if i == 0:
        continue
    jsonBody["songName"] = "{}.mp3".format(i)
    jsonBody["songCode"] = "10{}".format(i)
    jsonBody["description"] = "Número {}".format(i)
    print("jsonBody: {}".format(jsonBody))
    r = requests.post('https://us-central1-raspberry-instants.cloudfunctions.net/botonera/song/add', json=jsonBody)
    print("Status code: {}".format(r.status_code))
    time.sleep(1)