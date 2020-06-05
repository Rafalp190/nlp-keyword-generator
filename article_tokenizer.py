import pickle
import pandas as pd
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import train_test_split


def read_data_fragment(ftopic, directory=""):
    """ 
    Reads a pickle of articles and collects the topic and abstract of all papers that have it.
    Discards the rest because they can't be used to train the algorithm.
    ...........
    Parameters:
    -----------
    ftopic: str
        Topic of the pickle without spaces (utilizes the complete query)
    directory: str
        Path to the file.
    """
    with open(directory+'all_articles_on'+ftopic+'.pkl', 'rb') as f:
        data = pickle.load(f)

    usable_data = []
    for j in data:
        for i in j['data']:
            if i['topics'] != []:
                try:
                    usable_data.append((i['description'].lower(), i['topics']))
                except KeyError:
                    
                    print('No Abstract for article {}'.format(i['title']))
    return usable_data

def text_tokenizer(abstract):
    """ 
    Utilizes nltk's TreebankWordTokenizer to create tokens for each word and punctuation sign in an abstract. 
    ...........
    Parameters:
    -----------
    abstract: str
        Abstract of article to tokenize
    """
    tokenizer = TreebankWordTokenizer()
    return tokenizer.tokenize(abstract)


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
         #'social AND media'
]

# Create an empty dataframe to fit the columns
df = pd.DataFrame(columns=['Abstract', 'Topics']) 
# Gather all topics into a single dataframe
for topic in topics:
    ftopic = topic.replace(" ","")
    data_fragment = read_data_fragment(ftopic, "./raw_data/")
    topic_df = pd.DataFrame.from_records(data_fragment, columns=['Abstract', 'Topics']) 
    df = df.append(topic_df)

#Tokenizes the abstract
#df.Abstract = df.Abstract.map(lambda x: text_tokenizer(x))
df.to_csv("./cured_data/dataset.csv")
#df.Topics = df.Topics.map(lambda x: print(type(x)))
#print(data_df.head())

train, test = train_test_split(df, test_size=0.2, random_state=1)
train, val = train_test_split(train, test_size=0.25, random_state=1)
train.to_csv("./cured_data/train.csv")
test.to_csv("./cured_data/test.csv")
val.to_csv("./cured_data/val.csv")
