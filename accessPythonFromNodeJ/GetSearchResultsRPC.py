import zerorpc
from pymongo import MongoClient
import json
from bson import json_util
import random
from SearchModule import Search
from Statistics import Statistics
import sys
#the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('../TextZusammenfassung')
from WordExtractor import extractWordembeddings
from Summary import unpackAndSummarize
sys.path.append('../accessPythonFromNodeJ')
from bson import ObjectId




import GetWord2Vec



class GetSearchResultsRPC():

    def __init__(self):
        global collectionMongo 
        databaseMongo = MongoClient("127.0.0.1:27017").crawlerdb_WORK_TFIDF_3
        global search
        search = Search(databaseMongo)
        global stat
        stat = Statistics(set_dummy_data=True)
        
        
        global embeddings
        embeddings = extractWordembeddings()
        print("Embeddings length: ",len(embeddings))
        
        
        global getword2vec
        getword2vec = GetWord2Vec.GetWord2Vec()
     
        
        
        
    '''
    @author Marcel, Micha
    @version 0.2

    # Word2Vec WordEmbeddings
    # @param self obj  und suchString als Suchstring ("Haus und Auto" oder "König, Königin und Bärtige !!!!"))
    # @return JSONdump
    '''    
    def word2vec_similarity(self, searchString):
        return json.dumps(self.getword2vec.getword2vec(searchString), sort_keys=True, ensure_ascii=False, indent=4, default=json_util.default)
        
        
    def get_results(self, searchString,dateFROM,dateTO):
        print(searchString) # e.g. halloIch bin ein Suchstring
        print(dateFROM) # e.g. Tue Jan 08 2019 12:00:00 GMT+0100 (Central European Standard Time) # wenn nicht vorhanden: None
        print(dateTO) # e.g. Tue Jan 08 2019 12:00:00 GMT+0100 (Central European Standard Time)
        
        stat.write_search_term_to_db(searchString, printflag=True)
        
        # data muss eine liste / Array sein (kann geändert werden, erfordert aber eine Änderung im Backend)
        
        
        
        data = search.get_search_results(searchString)
        
        unpackAndSummarize(data,embeddings) # Added Field to data inplace
        
        
        
        synonyme = getword2vec.getword2vec(searchString)
        result = {"data": data, "synonyme": synonyme}
        
        # der return sollte vielleicht auf maximal 20 Elemente beschränkt sein
        return json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4, default=json_util.default)
    
    
    # called via /api/statistics   
    def get_articles_longer_read_than_4_s(self): # Format of list: [['object_id', count], ['object_id', count], ['object_id', count]]
        return stat.get_top_read_articles()
    

    # returned außerdem get_articles_longer_read_then_4_s
    def get_searched_words(self):
        result_list = stat.get_top_search_terms(printflag=False) # Format of list: [['word', count], ['word', count], ['word', count]]
        result_articles_ids_with_counter = stat.get_top_read_articles()
        print("output")
        if not result_articles_ids_with_counter:
            result_articles_ids_with_counter = []
        result = {"most_often_search_words": result_list, "result_articles_ids_with_counter": result_articles_ids_with_counter}
        #result = [result_list,result_articles_ids_with_counter]
        return json.dumps(result, sort_keys=True,ensure_ascii=False,indent=4,default=json_util.default)
        
        
        
        
        
    # called when user leave the page
    def write_articles_longer_read_than_4_s(self,results_object_ids):
        print("write")
        id = [results_object_ids]
        print(id)
        stat.write_read_articles_to_db(id)
        
        
        

        


def main():
    s = zerorpc.Server(GetSearchResultsRPC())
    s.bind("tcp://*:4242")
    s.run()

if __name__ == "__main__" : main()
