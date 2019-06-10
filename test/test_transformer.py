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
