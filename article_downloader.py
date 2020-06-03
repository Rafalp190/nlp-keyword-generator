import urllib.request
import urllib.parse
import json
import pprint
import pickle


class CoreApiRequestor:
    """
    Core Database API functions taken from the official Core API python example. 
    https://github.com/oacore/or2016-api-demo/blob/master/OR2016%20API%20demo.ipynb
    This function handles the API interfacing.
    ...

    Attributes
    ----------
    endpoint: str
        what part of the api you are connecting to.
    api_key: str
        Access key to be able to connect to the API
    
    Methods
    -------
    parse_response(decoded): 
        Turns the response into a dictionary
    request_url(url): 
        Makes the api request to the url of the site
    get_method_query_request_url(method,query,fullText,page):
        constructs the URL to make the request to
    get_up_to_30_pages_of_query(self,method,query,fulltext):
        iteratively gathers 30 pages of 100 results if available. 
        If there arent enough it pulls as many as possible. Rounded down to the nearest 100's.
    """
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key
        #defaults
        self.pagesize = 100
        self.page = 1

    def parse_response(self, decoded):
        res = []
        for item in decoded['data']:
            doi = None
            if 'identifiers' in item:
                for identifier in item['identifiers']:
                    if identifier and identifier.startswith('doi:'):
                        doi = identifier
                        break
            res.append([item['title'], doi])
        return res

    def request_url(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read()
        except urllib.error.HTTPError:
            print("Error 500 Trying again")
            with urllib.request.urlopen(url) as response:
                html = response.read()
        return html

    def get_method_query_request_url(self,method,query,fullText,page):
        if (fullText):
            fullText = 'true'
        else:
            fullText = 'false'
        params = {
            'apiKey':self.api_key,
            'page':page,
            'pageSize':self.pagesize,
            'fulltext':fullText
        }
        return self.endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params)

    def get_up_to_30_pages_of_query(self,method,query,fulltext):
        url = self.get_method_query_request_url(method,query,fulltext,1)
        all_articles=[]
        resp = self.request_url(url)
        result = json.loads(resp.decode('utf-8'))
        all_articles.append(result)
        if (result['totalHits']>100):
            numOfPages = int(result['totalHits']/self.pagesize)  #rounds down
            if (numOfPages>30):
                numOfPages=30
            for i in range(2,numOfPages):
                url = self.get_method_query_request_url(method,query,False,i)
                print(i)
                resp =self.request_url(url)
                all_articles.append(json.loads(resp.decode('utf-8')))
        return all_articles


'''
Example invokation
'''
# init 
endpoint = 'https://core.ac.uk/api-v2'

'''
********************************************
Add your own api key below
'''
api_key = 'ROxPlabFKhq6jDo8ksWUrEn2QHXp0VvJ'
'''
********************************************
'''
method = '/articles/search'
topics = ['biology',
         'computer AND science',
         'medicine',
         'cancer',
         'anthropology AND sociology',
         'biochemistry',
         'behavioural sciences',
         'history',
         'psychology',
         'archaeology',
         'paleontology',
         'math',
         'physics',
         'artificial AND intelligence',
         'machine AND learning',
         'videogames',
         'histology',
         'mechanics',
         'astronomy',
         'development',
         'economy',
         'statistics',
         'telemedicine',
         'literature',
         'ecology',
         'geology',
         'art',
         'virus AND disease',
         'coronavirus',
         'social AND media',
         'epidemiology'
]
        

api = CoreApiRequestor(endpoint,api_key)

'''
Get url
'''
#url = api.get_method_query_request_url(method,topic,False,1)
#print(url)
'''
Get results
'''
#Gets all the data and saves it to pickles by topic
for topic in topics:
    ftopic = topic.replace(" ","")
    queryOnlyFT = '(title:('+topic+') OR description:('+topic+') OR fullText:('+topic+')) AND fullText:*'
    query = '(title:('+topic+') OR description:('+topic+') OR fullText:('+topic+'))'

    # fetch all articles (with or without fulltext) matching topic query in title or abstract or fulltext
    try:
        all_articles = pickle.load(open('all_articles_on'+ftopic+'.pkl','rb'))
    except (OSError,IOError) as e:
        all_articles = api.get_up_to_30_pages_of_query(method,query,False)
        pickle.dump(all_articles,open('all_articles_on'+ftopic+'.pkl','wb'),pickle.HIGHEST_PROTOCOL)
