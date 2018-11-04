from google.cloud import speech_v1
from google.oauth2 import service_account
from . import recordtest
import six
import os

module_dir = os.path.dirname(__file__)
<<<<<<< HEAD
file_path = os.path.join(module_dir, "ventmo-e430325bdb43.json")
credentials = service_account.Credentials.from_service_account_file(file_path)
client = speech_v1.SpeechClient(credentials = credentials)
=======
>>>>>>> 4f41a88c03a11bc2ec8a6c7fe914f04a03511e3e

def run():
    test_path = os.path.join(module_dir, 'test.wav')
    file_path = os.path.join(module_dir, 'ventmo-e430325bdb43.json')
    credentials = service_account.Credentials.from_service_account_file(file_path)
    client = speech_v1.SpeechClient(credentials = credentials)

    language_code = 'en-US'
    config = {'language_code': language_code}

    rec = recordtest.Recorder()
    with rec.open(test_path, 'wb') as recfile:
        recfile.record(duration=10.0)
