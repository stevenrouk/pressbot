from collections import Counter
from functools import wraps
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer, TfidfVectorizer
import string

class Document(str):
    
    def __init__(self, text):
        self.text = text
        translator = str.maketrans({key: None for key in string.punctuation})
        without_punc = self.text.translate(translator)
        self.text_without_punc = without_punc.lower()
        self.words = self.text_without_punc.split()
        self.words_without_stop = [word for word in self.words if word not in ENGLISH_STOP_WORDS]
        self.word_counts = Counter(self.words_without_stop)
        sent_analyzer = SentimentIntensityAnalyzer()
        self.word_sentiments = {word: sent_analyzer.polarity_scores(word) for word in self.words_without_stop}
        self._word_sentiments_dict = self.word_sentiments
        self._word_sentiments_list = [[key, self.word_sentiments[key]] for key in self.word_sentiments.keys()]
        self._word_sentiments_negative = [x for x in self._word_sentiments_list if x[1]['neg']==1]
        self._word_sentiments_negative_sorted = sorted(self._word_sentiments_negative, key=lambda x: x[1]['compound'])
        #self._word_sentiments_positive = 
        #self._word_sentiments_compound = 
    
    def __repr__(self):
        return 'Document(\'{}\')'.format(self.text)

    def get_negative_words(self, n=5):
        return self._word_sentiments_negative_sorted[:n]

    def get_positive_words(self):
        pass

    def get_sentiment_compound(self):
        pass

class DocumentCorpus:
    
    def __init__(self, document_list=[]):
        self.documents = [Document(doc) for doc in document_list]
        self.analyze()
        self.analyzed = True

    def __len__(self):
        return len(self.documents)
    
    def _check_analyzed(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            inst.check_analyzed()
            return f(inst, *args, **kwargs)
        return wrapped
    
    def check_analyzed(self):
        if not self.analyzed:
            self.analyze()
    
    def analyze(self):
        self.all_words = [word for doc in self.documents for word in doc.words]
        self.terms = set(self.all_words)
        self.cv = self.setup_cv()
        self.term_frequency_matrix = self.cv.fit_transform(self.documents)
        self.tfidf = self.setup_tfidf()
        self.tfidf_matrix = TfidfVectorizer(decode_error='ignore', stop_words='english').fit_transform(self.documents)
        self.pairwise_similarity = self.tfidf_matrix * self.tfidf_matrix.T
        self.analyzed = True
    
    def __getitem__(self, key):
        return self.documents[key]
    
    def __setitem__(self, key, value):
        self.documents[key] = value
        self.analyzed = False
    
    def __repr__(self):
        document_strings = []
        for doc in self.documents:
            document_strings.append('\n\t\'{}\''.format(doc))
        return 'DocumentList({0}{1})'.format(''.join(document_strings), '\n' if document_strings else '')

    def setup_cv(self):
        cv = CountVectorizer(stop_words='english')
        cv.fit(self.documents)
        return cv
    
    def setup_tfidf(self):
        tfidf = TfidfVectorizer(decode_error='ignore', stop_words='english')
        tfidf.fit(self.documents)
        return tfidf
    
    def sort_sparse(self, m):
        m_coo = m.tocoo()
        rows = ['d{}'.format(x) for x in m_coo.row+1]
        cols = ['d{}'.format(x) for x in m_coo.col+1]
        tuples = zip(rows, cols, m_coo.data)
        
        return sorted(tuples, key=lambda x: (x[2]), reverse=True)
    
    @_check_analyzed
    def get_word_counts(self):
        feature_names = self.cv.get_feature_names()
        counts = [x.sum() for x in self.term_frequency_matrix.todense().T]
        
        return sorted(zip(feature_names, counts), key=lambda x: (x[1]), reverse=True)
    
    @_check_analyzed
    def plot_similarity_matrix(self):
        sns.heatmap((self.pairwise_similarity).todense())
    
    @_check_analyzed
    def get_term_freq_matrix(self):
        indices = ['d{}'.format(i) for i in range(1, len(self.documents) + 1)]
        df = pd.DataFrame(self.term_frequency_matrix.todense().T, index=self.tfidf.get_feature_names(), columns=indices)

        return df
    
    @_check_analyzed
    def get_tfidf_matrix(self):
        indices = ['d{}'.format(i) for i in range(1, len(self.documents) + 1)]
        df = pd.DataFrame(self.tfidf_matrix.todense().T, index=self.tfidf.get_feature_names(), columns=indices)

        return df
    
    @_check_analyzed
    def get_sorted_pairwise_similarity(self):
        return self.sort_sparse(self.pairwise_similarity)
    
    def add(self, document):
        self.documents.append(Document(document))
        self.analyzed = False

VIOLENT_TERMS = ['clubbed',
    'horrifying',
    'deformities',
    'cutting',
    'worst',
    'starve',
    'unethically',
    'concrete',
    'slammed',
    'reserved',
    'mutilated',
    'captured',
    'tortured',
    'broken',
    'pummeling',
    'shackling',
    'stunning',
    'killed',
    'abused',
    'spike',
    'aborting',
    'died',
    'tossing',
    'electrical',
    'shoving',
    'prodding',
    'slaughter',
    'weakley',
    'mistreating',
    'mistreatment',
    'beating',
    'tearing',
    'abusive',
    'violence”',
    'slaughtered',
    'maimed',
    'slit',
    'stick',
    'severed',
    'sticks',
    'knock',
    'bodies',
    'sickly',
    'bleed',
    'capture',
    'liveshackle',
    'die',
    'crates',
    'ghetto',
    'shake',
    'abusers',
    'shackles',
    'factories',
    'pulling',
    'mutilating',
    'aborted',
    'graphically',
    'organs',
    'horrified',
    'outraged',
    'liver',
    'bludgeoning',
    'beaten',
    'appalling',
    'swinging',
    'battery',
    'torturing',
    'torture',
    'abuses',
    'confined',
    'painful',
    'violate',
    'skeletal',
    'cuts',
    'processing',
    'dumped',
    'handling',
    'limb',
    'euthanize',
    'blade',
    'capturing',
    'smokehouse',
    'ties',
    'gruesome',
    'targeted',
    'antianimal',
    'chains',
    'meatproducing',
    'meatbuying',
    'bloodied',
    'stunned',
    'waste',
    'burn',
    'cruel',
    'graphic',
    'deformed',
    'violated',
    'suffering',
    'trap',
    'terrible',
    'ripping',
    'abortion',
    'brutal',
    'metal',
    'tumors',
    'tortures',
    'throwing',
    'pulled',
    'aggressive',
    'plead',
    'dead',
    'killing”',
    'unconscious',
    'help',
    'spiky',
    'slap',
    'gory',
    'crammed',
    'suffer',
    'maimed”',
    'jabbing',
    'damage',
    'abuse',
    'slump',
    'ripped',
    'injured',
    'sick',
    'horrific',
    'harsh',
    'punished',
    'punching',
    'deplorable',
    'stomping',
    'breeding',
    'stabbing',
    'shocking',
    'pounding',
    'hang',
    'striking',
    'violence',
    'hitting',
    'death',
    'shackled',
    'abusing',
    'chain”',
    'stunning”',
    'suffocate',
    'stuffing',
    'shock',
    'spearing',
    'jammed',
    'assault',
    'slitting',
    'electric',
    'cramped',
    'hung',
    'crushed',
    'cruelty',
    'packed',
    'inhumane',
    'mistreats',
    'crippled',
    'slaughterhouse',
    'meat',
    'limping',
    'hate'
]