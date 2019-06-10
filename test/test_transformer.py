import unittest
from numpy import linalg as LA
from transformer import LabelEncoder, TFIDFVectorizer

class TestLabelEncoder(unittest.TestCase):
    def test_transform(self):
        encoder = LabelEncoder()
        labels = list('ABCD')
        encoder.fit(labels)
        self.assertListEqual(list(encoder.transform(labels)), [0, 1, 2, 3])

    def test_inverse_transform(self):
        encoder = LabelEncoder()
        labels = list('ABCD')
        encoder.fit(labels)
        encoded_labels = encoder.transform(labels)
        self.assertListEqual(list(encoder.inverse_transform(encoded_labels)), labels)

    def test_load_save(self):
        encoder = LabelEncoder()
        labels = list('ABCD')
        encoder.fit(labels)
        address = 'temp/label_encoder.cod'
        encoder.save(address)
        new_encoder = LabelEncoder.load(address)
        self.assertListEqual(list(encoder.transform(labels)),
                             list(new_encoder.transform(labels)))

class TestTFIDFVectorizer(unittest.TestCase):
    def setUp(self):
        self.vectorizer = TFIDFVectorizer()
        self.corpus = ['This is the first document.',
                       'This document is the second document.',
                       'And this is the third one.',
                       'Is this the first document?']
        self.vectorizer.fit(self.corpus)

    def test_fit(self):
        feature_names = ['and', 'document', 'first', 'is', 'one', 'second',
                         'the', 'third', 'this']
        self.assertListEqual(list(self.vectorizer.get_feature_names()),
                             feature_names)

    def test_transform(self):
        X = self.vectorizer.transform(self.corpus)
        self.assertTupleEqual((X.shape), (4, 9))

    def test_load_save(self):
        address = 'temp/vectorizer.cod'
        self.vectorizer.save(address)
        new_vectorizer = TFIDFVectorizer.load(address)
        self.assertListEqual(list(self.vectorizer.get_feature_names()),
                             list(new_vectorizer.get_feature_names()))
        X1 = self.vectorizer.transform(self.corpus)
        X2 = new_vectorizer.transform(self.corpus)
        self.assertAlmostEqual(LA.norm(X1.todense()), LA.norm(X2.todense()))
