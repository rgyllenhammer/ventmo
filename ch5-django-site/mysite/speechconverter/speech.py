from google.cloud import speech_v1
from google.cloud import language
#from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
from google.cloud.speech import types
from google.cloud.language import enums
from google.cloud.language import types as langtypes
#from recordtest import Recorder
#from recordtest import RecordingFile
import six
import os

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'ventmo-e430325bdb43.json')
credentials = service_account.Credentials.from_service_account_file(file_path)
client = speech_v1.SpeechClient(credentials = credentials)
langclient = language.LanguageServiceClient(credentials = credentials)



#encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
#sample_rate_hertz = 16600
def run():
    language_code = 'en-US'
    config = {'language_code': language_code}

     #rec = Recorder()
     #text = input("enter s to start >> ")  # Python 3
     #if text == 's':
        #  with rec.open('test.wav', 'wb') as recfile:
        #      print("recording for 5 seconds")
        #      recfile.record(duration=5.0)

    file_name = os.path.join(module_dir, 'test.wav')

    # Loads the audio into memory
    with open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    response = client.recognize(config, audio)
    text = ''
    for result in response.results:
        s = 'Transcript: {}'.format(result.alternatives[0].transcript)
        text += '{}'.format(result.alternatives[0].transcript)

    f = open(os.path.join(module_dir, 'textfiles/file_in.txt'), 'w+')
    f.write(text)
    f.close()
