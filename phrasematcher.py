import tweepy
import spacy
import time
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')


phrasematcher = PhraseMatcher(nlp.vocab)

phrase_list1 = ['how you doing', 'how are you', 'hope everything is fine']
phrase_list2 = ['what is your name', 'how are you called','what can i call you']
phrase_list3 = ['who created you','creator','made you','developed']
phrase_list4 = ['live','location']
phrase_list5 = ['weather','season']
phrase_list6 = ['how old are you','what is your age','how many years']

# Next, convert each phrase to a Doc object:
phrase_patterns1 = [nlp(text) for text in phrase_list1]
phrase_patterns2 = [nlp(text) for text in phrase_list2]
phrase_patterns3 = [nlp(text) for text in phrase_list3]
phrase_patterns4 = [nlp(text) for text in phrase_list4]
phrase_patterns5 = [nlp(text) for text in phrase_list5]
phrase_patterns6 = [nlp(text) for text in phrase_list6]

# Pass each Doc object into matcher (note the use of the asterisk!):
phrasematcher.add('Emotion', None, *phrase_patterns1)
phrasematcher.add('Name', None, *phrase_patterns2)
phrasematcher.add('Creator', None, *phrase_patterns3)
phrasematcher.add('Location', None, *phrase_patterns4)
phrasematcher.add('Season', None, *phrase_patterns5)
phrasematcher.add('Age', None, *phrase_patterns6)



CONSUMER_KEY = '7weLAT5g8kGIZKRKzrobqxYWF'
CONSUMER_SECRET = 'h6qZQ1BOJKAJhWTov4ZdOQoOFo3cZAeLpL9HpFliPZTpJDMklb'
ACCESS_KEY = '1231308506919124992-lbE8acHJxbr0p3235mZZnVLRuQwMjV'
ACCESS_SECRET = '4QVUZrjXnRLGtCd5fGXojyw6e4XjD0xiBvHryTEzpQr3y'
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name,'r')
    try:
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id
    except:
        pass

def store_last_seen_id(last_seen_id,file_name):
    f_write = open(file_name,'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    print('6')
    mentions =  api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in mentions:
        print(str(mention.id) + ' - ' +  mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FILE_NAME)
        if '#askme' in mention.full_text.lower():
            temp = str(mention.full_text.lower())
            doc = nlp(temp)
            print(doc)
            found_matches = phrasematcher(doc)
            print(found_matches)
            for match_id,start,end in found_matches:
                string_id = nlp.vocab.strings[match_id]
                print(string_id)
                if string_id == 'Name':
                    api.update_status('@'+ mention.user.screen_name + '  Hi, My name is Rosy',mention.id)
                if string_id == 'Age':
                    api.update_status('@'+ mention.user.screen_name + ' I am a second older than you!',mention.id)
                if string_id == 'Emotion':
                    api.update_status('@'+ mention.user.screen_name + ' I am great as usual',mention.id)
                if string_id == 'Creator':
                    api.update_status('@'+ mention.user.screen_name + ' I am the creator of my own!',mention.id)
                if string_id == 'Season':
                    api.update_status('@'+ mention.user.screen_name + ' The weather here is windy and pretty cool',mention.id)
                if string_id == 'Location':
                    api.update_status('@'+ mention.user.screen_name + ' I am Omnipresent!:) ',mention.id)
                if string_id == 'Greet':
                    api.update_status('@'+ mention.user.screen_name + ' Namaste, Hope you are doing good ',mention.id)
                
while True:
    reply_to_tweets()
    
