from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import six


credentials = service_account.Credentials.from_service_account_file("voice-test-afb02ccbc45b.json")
client = language.LanguageServiceClient(credentials = credentials)
text = "I love bananas but I dislike eggplants"

if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

document = types.Document(
    content=text,
    type = enums.Document.Type.PLAIN_TEXT
)
encoding = enums.EncodingType.UTF32

result = client.analyze_entity_sentiment(document, encoding)

sentiment = client.analyze_sentiment(document=document).document_sentiment
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
