import pymongo
import json
from bson import json_util
import Preprocessor
import pprint
import re

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017


preprocessor = Preprocessor.Preprocessor()

connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
MONGODB_DB = "crawlerdb_BACKUP"
db = connection[MONGODB_DB]

MONGODB_COLLECTION = "crawlerdb_BACKUP"
collection = db[MONGODB_COLLECTION]

MONGODB_COLLECTION_TOKENIZING = "crawlerdb_tokenization"
MONGODB_COLLECTION_STEMMING = "crawlerdb_stemming"
collection_stemm = db[MONGODB_COLLECTION_STEMMING]
collection_token = db[MONGODB_COLLECTION_TOKENIZING]


MONGODB_COLLECTION_WITHSW = "crawlerdb_withSW"
MONGODB_COLLECTION_WITHOUTSW = "crawlerdb_withoutSW"
collection_with_stopwords = db[MONGODB_COLLECTION_WITHSW]
collection_without_stopwords =db[MONGODB_COLLECTION_WITHOUTSW]

MONGODB_COLLECTION_WITHOUTSW_WITHUMLAUTE = "crawlerdb_withUmlaute_withoutSW"
collection_without_stopwords_with_umlaute = db[MONGODB_COLLECTION_WITHOUTSW_WITHUMLAUTE]

MONGODB_COLLECTION_WITHSW_WITHUMLAUTE = "crawlerdb_withUmlaute_withSW"
collection_with_stopwords_with_umlaute = db[MONGODB_COLLECTION_WITHSW_WITHUMLAUTE]

preprocessor = Preprocessor.Preprocessor()


def remove_double_records(listObj):
    x = []
    n = []
    for e in listObj:
        if e not in x:
            n.append(e)
            x.append(e)
    return n


########## ROHDATEN ##########
''' 
{
    'number': '1288202', 
    'location': 'Cottbus', 
    'text': 'Nach einem Fehler beim Überholen....', 
    'date': '14.12.2018', 
    '_id': ObjectId('5c2fc96788df4228e7861c93'), 
    'title': 'Fehler beim Überholen'
}
'''
########## LOWER, STOPWORDS AND PUNCTIONAL REMOVING + TOKEN AND STEMMING ##########
''' 
{
    'number': '1288202', 
    'stemming_text': ['','' .... ], 
    'stemming_title': ['','' .... ], 
    '_id': ObjectId('5c2fc96788df4228e7861c93'), 
}
'''

########## LOWER, STOPWORDS AND PUNCTIONAL REMOVING + TOKEN AND LEMMATIZATION ##########
'''
{
    'number': '1288202', 
    'lemmatization_title': [{'',''},{'',''}], 
    'lemmatization_text': [{'',''},{'',''}],
    '_id': ObjectId('5c2fc96788df4228e7861c93'),
}
'''

########## LOWER, STOPWORDS AND PUNCTIONAL REMOVING + TOKEN AND LEMMATIZATION ##########
'''
{
    'number': '1288202', 
    'lemmatization_title': [{'',''},{'',''}], 
    'lemmatization_text': [{'',''},{'',''}],
    '_id': ObjectId('5c2fc96788df4228e7861c93'),
}
'''
var1=0
jsonobjStemming = {
    "number": "",
    "stemming_text": { "stemming_text_words": [], },
    "stemming_title": { "stemming_title_words": [], },
    }

jsonobjTokenizing = {
    "number": "",
    "token_text": { "token_text_words": [], },
    "token_title": { "token_title_words": [], },
    }

mylistStemm = []
mylistToken = []

dataToken={}
dataStemm={}
dataPunc={}
dataPuncSW={}

i=0
g=0
l=[]

#collection_stemm.drop()
#collection_token.drop()

for doc in collection.find():
    g=g+1
    if "_id" in doc and "number" in doc and "text" in doc and "title" in doc:
        i=i+1
        numberstring = str(doc["number"])
        numbertoken = re.search("[0-9]+", numberstring)
        #print(numbertoken.group())
        number=numbertoken.group()
        
        ###### REMOVING PUNCTIONAL AND STOPWORDS AND MAKE TOKENS ############
        token_text = preprocessor.tokenizing_complete(doc["text"])
        token_title = preprocessor.tokenizing_complete(doc["title"])
        dataToken["number"]=number
        dataToken["token_text"] = token_text
        dataToken["token_title"] = token_title
        jsonobjreadyToken = dataToken
        try:
            collection_token.insert(jsonobjreadyToken)
        except Exception as exception:
        # Output unexpected Exceptions.
            print("find an dublicate in TOKEN_Collection")
            #Logging.log_exception(exception, False)
        
        #mylistToken.append(jsonobjreadyToken)
        ############ STEMMING THE TOKENS ################
        stemm_text = preprocessor.stemming_words(token_text)
        stemm_title = preprocessor.stemming_words(token_title)
        dataStemm["number"]=number
        dataStemm["token_text"] = stemm_text
        dataStemm["token_title"] = stemm_title
        jsonobjreadyStemm = dataStemm
        try:
            collection_stemm.insert(jsonobjreadyStemm)
        except Exception as exception:
            print("find an dublicate in STEMM_Collection")
            #Logging.log_exception(exception, False)
        
        ###### REMOVING PUNCTIONAL ############
        puncremove_text = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc(doc["text"]))
        puncremove_title = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc(doc["title"]))
        dataPunc["number"] = number
        dataPunc["title"] = puncremove_title
        dataPunc["text"] = puncremove_text
        jsonobjreadyPunc = dataPunc
        try:
            collection_with_stopwords.insert(jsonobjreadyPunc)    
        except Exception as exception:
            print("find an dublicate in PUNCREMOVE_Collection")
            #Logging.log_exception(exception, False)
        
        ###### REMOVING PUNCTIONAL AND STOPWORDS ############
        punc_sw_remove_text = preprocessor.tokenizing_reverse(preprocessor.tokenizing_complete(doc["text"]))
        punc_sw_remove_title = preprocessor.tokenizing_reverse(preprocessor.tokenizing_complete(doc["title"]))
        dataPuncSW["number"] = number
        dataPuncSW["title"] = punc_sw_remove_title
        dataPuncSW["text"] = punc_sw_remove_text
        jsonobjreadyPuncSw = dataPuncSW
              
        try:
            collection_without_stopwords.insert(jsonobjreadyPuncSw)    
        except Exception as exception:
            print("find an dublicate in PUNC_AND_SW_REMOVE_Collection")
            #Logging.log_exception(exception, False)

        ###### WITH UMLAUT BUT REMOVING PUNCTIONAL ############
        puncremove_umlaute_text = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc_with_umlaute_sw(doc["text"]))
        puncremove_umlaute_title = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc_with_umlaute_sw(doc["title"]))
        dataPunc["number"] = number
        dataPunc["title"] = puncremove_umlaute_title
        dataPunc["text"] = puncremove_umlaute_text
        jsonobjreadyPunc = dataPunc
        try:
            
            collection_with_stopwords_with_umlaute.insert(jsonobjreadyPunc)    
        except Exception as exception:
            print("find an dublicate in WITH_UMLAUTE_AND_SW_WITHOUT_PUNCREMOVE_Collection")
            #Logging.log_exception(exception, False)
        
        ###### WITH UMLAUT BUT REMOVING PUNCTIONAL AND STOPWORDS  ############
        punc_sw_umlaute_text = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc_and_sw_with_umlaute(doc["text"]))
        punc_sw_umlaute_title = preprocessor.tokenizing_reverse(preprocessor.tokenizing_without_punc_and_sw_with_umlaute(doc["title"]))
        dataPuncSW["number"] = number
        dataPuncSW["title"] = punc_sw_umlaute_title
        dataPuncSW["text"] = punc_sw_umlaute_text
        jsonobjreadyPuncSw = dataPuncSW
              
        try:
            collection_without_stopwords_with_umlaute.insert(jsonobjreadyPuncSw)    
        except Exception as exception:
            print("find an dublicate in WITH_UMLAUTE_WITHOUT_PUNC_AND_SW_REMOVE_Collection")
            #Logging.log_exception(exception, False)
        
        #mylistStemm.append(jsonobjreadyStemm)
        l.append(number)

    #print(i)
    #print(doc)
    x = doc
    #print(x)
    #print(x['number'])
    #print(x['title'])
    #print(x['text'])
    
    #token_title = preprocessor.tokenizing_complete(x['title'])
    #token_text = preprocessor.tokenizing_complete(x['text'])
    #token_number = re.search("[0-9]+", str(x['number']))
    #token_number = x['number']
    #thisdict =	dict(number=token_number, title=token_title, text=token_text)
    #print(thisdict)


print("records = " + str(g))
print("records with id and number = " + str(i))
#print(jsonobjStemming)
print(mylistStemm[0:15])
print(len(mylistStemm))

withoutDoubleData = remove_double_records(mylistStemm)
print(len(withoutDoubleData))
print(len(remove_double_records(l)))
print(len(l))


#ww = collection_token.insert_many(mylistToken)
#print list of the _id values of the inserted documents:
#print(ww.inserted_ids)

#qq = collection_stemm.insert_many(mylistStemm)
#print list of the _id values of the inserted documents:
#print(qq.inserted_ids)

for doc in collection_stemm.find():
    g=g+1
print("colelction_stemm length = ",str(g))

for doc in collection_token.find():
    g=g+1
print("colelction_token length = ",str(g))

for doc in collection_with_stopwords.find():
    g=g+1
print("colelction_with_SW  length = ",str(g))

for doc in collection_without_stopwords.find():
    g=g+1
print("colelction_withoutSW length = ",str(g))

'''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

mydict = { "name": "John", "address": "Highway 37" }
x = mycol.insert_one(mydict)

x = mycol.insert_many(mylist)
#print list of the _id values of the inserted documents:
print(x.inserted_ids)
'''



'''
jsonobj = {
          "a": {
              "b": {
                      "c": var1,
                      "d": var2,
                      "e": [],
                   },

                },
            }
###ebene runter gehen und anfuegen
jsobj["a"]["b"]["e"].append({"f":var3, "g":var4, "h":var5})
jsobj["a"]["b"]["e"].append({"f":var6, "g":var7, "h":var8})
'''

