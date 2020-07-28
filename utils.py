import os
import dialogflow_v2 as dialogflow
from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\SHITIJ\\PycharmProjects\\CodingBlocks13 - Telegram Bot\\client.json"
dialogflow_session_client = dialogflow.SessionsClient()
Project_ID = "news-bot-yunqam"


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(Project_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response1 = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response1.query_result


#we have created this function to receive the appropriate response from our bot
def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small talk", response.fulfillment_text


#we now create a function to fetch news for the corresponding query
#we use the gnewsclient created by Nikhil sir himself to fetch the relevant news
def fetch_news(parameters):
    client.topics.append('Music', 'Astronomy', 'Covid- 19')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    client.topic = parameters.get('news_topic')

    #we receive the parameters from using the dialogflow agent in this form
    #{'geo-country': 'India', 'news_topic': 'Business', 'language': ''}
    #our bot will extract data using these parameters

    return client.get_news()[:5]


topics_keyboard = [
    ['Top Stories', 'World', 'Nation'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science', 'Health']
    # ['Covid-19', 'Music', 'Astronomy']
    ]
