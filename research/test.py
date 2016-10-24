import bs4 as BeautifulSoup
import csv
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def create_similarity_matrix():
    with open('pressbotcity.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
    p_tags = soup.findAll('p')
    p_tags_text = [tag.text for tag in p_tags]
    article_text = [text.encode('utf-8', 'ignore') for text in p_tags_text]
    article_text = [text for text in article_text if 'Article ID' not in text and len(text) > 200]

    tfidf = TfidfVectorizer().fit_transform(article_text)
    pairwise_similarity = tfidf * tfidf.T

    with open('text.csv', 'wb') as f:
        csvwriter = csv.writer(f, lineterminator='\n')
        csvwriter.writerows(pairwise_similarity.A)


def term_frequency():
    train_set = ('hello there my friend', 'my friend is a really good man', "man I'm tired", "man oh man oh man am I really tired")
    vectorizer = CountVectorizer(stop_words='english')
    train_matrix = vectorizer.fit_transform(train_set)
    print vectorizer.vocabulary_
    print train_matrix
    print train_matrix.todense()


if __name__ == '__main__':
    term_frequency()
