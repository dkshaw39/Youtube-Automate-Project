import configparser
import requests
import json
import time

def generateAudio(config,txt):
    
    # API website to get your (free) key: https://rapidapi.com/k_1/api/large-text-to-speech/
    url = "https://large-text-to-speech.p.rapidapi.com/tts"
    payload = {"text": txt}

    headers = {
        "content-type": config['RapidAPI_Text_to_Speach']['type'],
        "X-RapidAPI-Key": config['RapidAPI_Text_to_Speach']['key'],
        "X-RapidAPI-Host": config['RapidAPI_Text_to_Speach']['host']
    }
    try:
        # POST request
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        #print(response.text)

        # get id and eta of the job from the response
        id = json.loads(response.text)['id']
        eta = json.loads(response.text)['eta']

        print(f'Waiting {eta} seconds for the job to finish...')
        time.sleep(eta)

        # GET the result from the API
        response = requests.request("GET", url, headers=headers, params={'id': id})
        # if url not returned yet, wait and try again
        while "url" not in json.loads(response.text):
            response = requests.get(url, headers=headers, params={'id': id})
            time.sleep(5)
        # if no error, get url and download the audio file
        if not "error" in json.loads(response.text):
            result_url = json.loads(response.text)['url']
            # download the waw file from results_url
            response = requests.get(result_url)
            # save the waw file to disk
            with open(config['path']['location']+'output.wav', 'wb') as f:
                f.write(response.content)
            print("File output.wav saved!")
        else:
            print(json.loads(response.text)['error'])
    except Exception as e:
        print(e)



if __name__== '__main__':
    ## Read Config file
    config_file = "config.init"
    config = configparser.ConfigParser()
    config.read(config_file)
    
    ##Read test file
    f=open(config['path']['location']+'crypto.txt','r')
    txt = f.read()
    f.close()

    ##generate Audio
    generateAudio(config,txt)
