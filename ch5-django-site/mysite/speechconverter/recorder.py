from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
from google.cloud.speech import types
from recordtest import Recorder
from recordtest import RecordingFile
import six
import os

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "ventmo-e430325bdb43.json")
credentials = service_account.Credentials.from_service_account_file(file_path)
client = speech_v1.SpeechClient(credentials = credentials)

language_code = 'en-US'
config = {'language_code': language_code}

rec = Recorder()
text = input("enter s to start >> ")  # Python 3
if text == 's':
    with rec.open('test.wav', 'wb') as recfile:
        print("recording for 5 seconds")
        recfile.record(duration=5.0)
