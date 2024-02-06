import requests
import json
import numpy as np
import boto3
import time
import random
import string
import hashlib
from scipy.io.wavfile import write
import os
from pydub import AudioSegment

def generate_audio(prompt, duration=20):

    API_URL = "https://z7rqldgty2m0ike1.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept" : "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json" 
    }
    payload = {
        "inputs": prompt,
        "parameters": {}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {
            "statusCode": 500,
            "body" : json.dumps({"error": "Music Gen Error 1"})
        }
    output = response.json()

    try:
        float_data = output[0]["generated_audio"][0]
    except:
        return {
            "statusCode": 500,
            "body" : json.dumps({"error": "Music Gen Error 2"})
        }

    numpy_data = np.array(float_data)
    numpy_data *= 32767
    numpy_data = numpy_data.astype(np.int16)
    key = generate_unique_key()

    filepath = "/tmp/" + key + ".wav"
    s3key = key + ".wav"

    write(filepath,  data=numpy_data, rate=32000)

    overwrite_first_n_seconds(filepath, duration)

    saveToS3(filepath, s3key)

    # os.remove("/tmp/" + key+".wav")

    return key

def saveToS3(file_name, filekey):
    key = "AKIAQJOTY2BOENJZM2VT"
    secret = "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"

    s3 = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret, region_name="ap-south-1")
    s3.upload_file(file_name, "techfest-mp3", filekey)
        
def generate_unique_key():
    timestamp = round(time.time() * 1000)
    random_str = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 16))
    full_str = str(timestamp) + random_str
    hash_object = hashlib.sha1(full_str.encode())
    hex_dig = hash_object.hexdigest() 

    return hex_dig

def generate_name(prompt):
    url = "https://1agnfox1re.execute-api.ap-south-1.amazonaws.com/Production/techfest-audio-namer"
    key = "WPzAZgh5lD97fuVIMtUwj2gaFE7bTtZ11qIThsQL"

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["name"]

def generate_genre(prompt):
    url = "https://1agnfox1re.execute-api.ap-south-1.amazonaws.com/Production/techfest-genre"
    key = "nnLMkw79ne4xidb1Mp3nzaq8BsbYAhht5YwVrSR7"

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["name"]

def get_url(s3key):
    key = "AKIAQJOTY2BOENJZM2VT"
    secret = "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"

    s3 = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret, region_name="ap-south-1")

    return s3.generate_presigned_url("get_object", Params={"Bucket": "techfest-mp3", "Key": s3key}, ExpiresIn=36000)


def generate_prompt(prompt, genre):
    url = "https://1agnfox1re.execute-api.ap-south-1.amazonaws.com/Production/techfest-prompt-engineer"
    key = "nnLMkw79ne4xidb1Mp3nzaq8BsbYAhht5YwVrSR7"

    headers = {
        "x-api-key": key
    }

    r = requests.post(url, headers=headers, json={"prompt": prompt, "genre": genre})
    return r.json()["prompt"]

def overwrite_first_n_seconds(file_path, duration_in_seconds):
    audio = AudioSegment.from_wav(file_path)
    n_seconds = duration_in_seconds * 1000 
    first_n_seconds = audio[:n_seconds]
    first_n_seconds.export(file_path, format="wav")
