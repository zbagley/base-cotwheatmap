import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import time
db = dataset.connect(settings.CONNECTION_STRING)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return

        ##TWEET TEXT AND CO-ORDS
        text = status.text
        coords = status.coordinates
        loc = status.place
        ##

        ##TextBlob for fast tweet analysis https://textblob.readthedocs.io/en/dev/index.html
        blob = TextBlob(text)
        blob = blob.lower()
        ##


        ##Add tweet co-ords to separate database for later clustering
        if coords is not None:
            if coords['coordinates'][0] > settings.CO_GEOBOX[0] and coords['coordinates'][0] < settings.CO_GEOBOX[2] and coords['coordinates'][1] < settings.CO_GEOBOX[3] and coords['coordinates'][1] > settings.CO_GEOBOX[1]:
                lng=coords['coordinates'][0]
                lat=coords['coordinates'][1]
                table2 = db[settings.TABLE2]
                try:
                    table2.insert(dict(
                        lat=lat,
                        lng=lng,
                        tm=time.time()
                    ))
                except ProgrammingError as err:
                    print(err)
        else:
            ##Add city/state location
            if loc is not None:
                loc = loc.bounding_box.coordinates
                lng_box = (loc[0][0][0] + loc[0][2][0])/2
                lat_box = (loc[0][0][1] + loc[0][2][1])/2
                if lng_box is not None:
                    if lng_box > settings.CO_GEOBOX[0] and lng_box < settings.CO_GEOBOX[2] and lat_box < settings.CO_GEOBOX[3] and lat_box > settings.CO_GEOBOX[1]:
                        table2 = db[settings.TABLE2]
                        try:
                            table2.insert(dict(
                                lat=lat_box,
                                lng=lng_box,
                                tm=time.time()
                            ))
                        except ProgrammingError as err:
                            print(err)




        ##Cross reference tweet words with required terms (nederland/eldora/skiing)
        if any(blob.find(settings.TERMS_SKI[x]) != -1 for x in range(len(settings.TERMS_SKI))):
            ##NLTK Sentiment Analysis http://www.nltk.org/howto/sentiment.html (Demo: http://text-processing.com/demo/sentiment/)
            sent = blob.sentiment
            table1 = db[settings.TABLE1]
            try:
                table1.insert(dict(
                    id_str=status.id_str,
                    polarity=sent.polarity,
                    subjectivity=sent.subjectivity,
                    tm=time.time()
                ))
            except ProgrammingError as err:
                print(err)
        ##


        ##Cross reference tweet words with required terms (nederland/eldora/skiing)
        if any(blob.find(settings.TERMS_NED[x]) != -1 for x in range(len(settings.TERMS_NED))):
            ##NLTK Sentiment Analysis http://www.nltk.org/howto/sentiment.html (Demo: http://text-processing.com/demo/sentiment/)
            sent = blob.sentiment
            table3 = db[settings.TABLE3]
            try:
                table3.insert(dict(
                    id_str=status.id_str,
                    polarity=sent.polarity,
                    subjectivity=sent.subjectivity,
                    text=text,
                    tm=time.time()
                ))
            except ProgrammingError as err:
                print(err)
        ##

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)
 
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(locations=settings.CO_GEOBOX)