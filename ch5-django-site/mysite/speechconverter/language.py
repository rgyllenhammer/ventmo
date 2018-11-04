from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import six
import os

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'ventmo-e430325bdb43.json')
credentials = service_account.Credentials.from_service_account_file(file_path)
client = language.LanguageServiceClient(credentials = credentials)

def return_sentiment(text):

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

    return_arr = []
    for entity in result.entities:
        ret_string = "\n\n\n==================\n"
        ret_string += 'Mentions: ' + u'Name: "{}"'.format(entity.name) + '\n\n'
        for mention in entity.mentions:
            ret_string += '  Begin Offset : {}'.format(mention.text.begin_offset) + '\n\n'
            ret_string += '  Content : {}'.format(mention.text.content) + '\n\n'
            ret_string += '  Magnitude : {}'.format(mention.sentiment.magnitude) + '\n\n'
            ret_string += '  Sentiment : {}'.format(mention.sentiment.score) + '\n\n'
            ret_string += '  Type : {}'.format(entity_type[mention.type]) + '\n\n'
        ret_string += 'Salience: {}'.format(entity.salience) + '\n\n'
        ret_string += 'Sentiment: {}\n'.format(entity.sentiment) + '\n\n'
        return_arr.append('SENTIMENT SCORE: {}'.format(sentiment.score) + '\n\n' + 'SENTIMENT MAGNITUDE: {}'.format(sentiment.magnitude) + '\n')

        return_arr.append(ret_string)

    return return_arr
