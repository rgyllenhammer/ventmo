from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import six
import os

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'ventmo-e430325bdb43.json')
credentials = service_account.Credentials.from_service_account_file(file_path)
client = language.LanguageServiceClient(credentials = credentials)

#takes in a list of dictionaries
#Example Doictionary:
#Entity{
# "Type" : String
#"Salience" : double
# "Sentiment": double
# "Magnitiude: double
#}
#return alist of 3 dictionaries
def three_Entities(entities):
	if len(entities) <= 10:
		return entities
	else:
		total = 3
		final_ents = []

		while total > 0:
			max_e = 0.0
			for entity in entities:
				if entity["salience"] > max_e:
					max_ent = entity
					max_e = entity["salience"]
			final_ents.append(max_ent)
			entities.remove(max_ent)
			total -= 1
	return final_ents

#takes in a sentiment value
def postive(s):
	if s >= .4:
		return True
	return False

def negative(s):
	if s <= -.4:
		return True
	return False

def nuetral(s):
	if s < .4 and s > -.4:
		return True
	return False

def max_mag(entities):
	max = 0
	for entitiy in entities:
		if entitiy["magnitude"] > max:
			max = entitiy["magnitude"]
	return max

final_sent = []
def three_sentences(entities):
	for entitiy in entities:
		if postive(entitiy["sentiment"]):
			if entitiy["magnitude"] > max_mag(entities)/1.5:
				final_sent.append("love " + entitiy["name"])
			else:
				final_sent.append("like " + entitiy["name"])
		elif negative(entitiy["sentiment"]):
			if entitiy["magnitude"] > max_mag(entities)/1.5:
				final_sent.append("hate " + entitiy["name"])
			else:
				final_sent.append("dislike " + entitiy["name"])
		else:
			if entitiy["magnitude"] > max_mag(entities)/1.5:
				final_sent.append("confused " + entitiy["name"])
			else:
				final_sent.append("neutral " + entitiy["name"])

	return final_sent


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

        entity_obj = {
            'name':entity.name,
            'sentiment':entity.sentiment.score,
            'salience':entity.salience,
            'magnitude':entity.sentiment.magnitude
        }
        return_arr.append(entity_obj)

    entity_list = three_Entities(return_arr)
    list_of_strings = three_sentences(entity_list)


    textToSearch = " ".join(list_of_strings)
    query_string = urllib.parse.urlencode({"search_query" : textToSearch})
    html = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    soup = BeautifulSoup(html, features="html.parser")
    vid = soup.find(attrs={'class':'yt-uix-tile-link'})
    print('https://www.youtube.com' + vid['href'])
    return list_of_strings
