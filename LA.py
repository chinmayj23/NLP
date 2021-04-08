from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import requests
import chatterbot
from tweets import twitter_analyze

#list_response=[]
#analyze=twitter_analyze()
#stocks = ['aapl', 'abfrl', 'stock','hdfc','reliance']
#for i in stocks:
 #   list_response.append(analyze.analyze_feelings(i))


class MyLogicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        
    def can_process(self, statement):
        words = [ 'hdfc bank', 'reliance', 'infosys', 'hdfc ltd', 'icici', 'tcs', 'kotak mahindra', 'hindustan unilever', 'axis bank', 'itc', 'l&t', 'sbi', 'airtel', 'bajaj', 'asian paints', 'hcl', 'maruti', 'm&m', 'ultratech', 'sun pharma', 'wipro', 'indusind bank', 'titan', 'bajaj finserv', 'nestle india', 'tata motors', 'tech mahindra', 'hdfc life insurance', 'power grid', 'dr reddys', 'tata steel', 'ntpc','hindalco', 'adani ports', 'bajaj auto', 'grasim', 'divis', 'hero motocorp', 'ongc', 'britannia', 'cipla', 'jsw steel', 'bpc', 'shree cement', 'eicher motors', 'sbi life insurance', 'coal india', 'upl', 'gail', 'indian oil']
        if any(x in statement.text.lower() for x in words):
            return True
        else:
            words.append(statement.text.lower())
            return False


    def process(self, input_statement,additional_response_selection_parameters=None):
         #stock=str(input_statement)
         analyze=twitter_analyze()        
         response=analyze.analyze_feelings(str(input_statement))
        #response=analyze
         #confidence=1
         response_statement=(Statement(response))
         return response_statement


        
         
