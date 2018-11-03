from google.cloud import speech_v1
from google.cloud import language
#from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
from google.cloud.speech import types
from google.cloud.language import enums
from google.cloud.language import types as langtypes
from recordtest import Recorder
from recordtest import RecordingFile
import six

credentials = service_account.Credentials.from_service_account_file("voice-test-afb02ccbc45b.json")
client = speech_v1.SpeechClient(credentials = credentials)
langclient = language.LanguageServiceClient(credentials = credentials)

#encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
#sample_rate_hertz = 16600
language_code = 'en-US'
config = {'language_code': language_code}
#uri = '../Documents/Sound recordings/test-voice.m4a'
#audio = {'uri': uri}
# The name of the audio file to transcribe
rec = Recorder()
text = input("enter s to start >> ")  # Python 3
if text == 's':
    with rec.open('test.wav', 'wb') as recfile:
        print("recording for 5 seconds")
        recfile.record(duration=5.0)
file_name = "test.wav"

# Loads the audio into memory
with open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

response = client.recognize(config, audio)
text = ''
for result in response.results:
    s = 'Transcript: {}'.format(result.alternatives[0].transcript)
    print(s)
    text += 'Transcript: {}'.format(result.alternatives[0].transcript)

if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

document = langtypes.Document(
    content=text,
    type = enums.Document.Type.PLAIN_TEXT
)
encoding = enums.EncodingType.UTF32

result = langclient.analyze_entity_sentiment(document, encoding)

sentiment = langclient.analyze_sentiment(document=document).document_sentiment
#response = client.analyze_entities(document=document)


# entity types from enums.Entity.Type
entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

for entity in result.entities:
    print('Mentions: ')
    print(u'Name: "{}"'.format(entity.name))
    for mention in entity.mentions:
        print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
        print(u'  Content : {}'.format(mention.text.content))
        print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
        print(u'  Sentiment : {}'.format(mention.sentiment.score))
        print(u'  Type : {}'.format(entity_type[mention.type]))
    print(u'Salience: {}'.format(entity.salience))
    print(u'Sentiment: {}\n'.format(entity.sentiment))

'''for entity in response.entities:
    print('=' * 20)
    print(u'{:<16}: {}'.format('name', entity.name))
    print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
    print(u'{:<16}: {}'.format('metadata', entity.metadata))
    print(u'{:<16}: {}'.format('salience', entity.salience))
    print(u'{:<16}: {}'.format('wikipedia_url',
          entity.metadata.get('wikipedia_url', '-')))
'''
print('Score: {}'.format(sentiment.score))
print('Magnitude: {}'.format(sentiment.magnitude))
