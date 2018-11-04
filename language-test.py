from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import six
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


credentials = service_account.Credentials.from_service_account_file("ventmo-e430325bdb43.json")
client = language.LanguageServiceClient(credentials = credentials)
text = "I hate bananas but I love bananas"

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

negative = []
positive = []

for entity in result.entities:
    print('Mentions: ')
    word = entity.name
    print(u'Name: "{}"'.format(entity.name))
    for mention in entity.mentions:
        print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
        print(u'  Content : {}'.format(mention.text.content))
        print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
        score = mention.sentiment.score
        if score > 0:
            positive.append(word)
        else:
            negative.append(word)
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

positives = ''
for i in range(len(negative)):
    print("You seem to dislike", negative[i])
for i in range(len(positive)):
    positives += positive[i]
    print("You seem to like", positive[i])

textToSearch = positives
query_string = urllib.parse.urlencode({"search_query" : textToSearch})
html = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
soup = BeautifulSoup(html)
vid = soup.find(attrs={'class':'yt-uix-tile-link'})
print('https://www.youtube.com' + vid['href'])
