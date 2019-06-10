'''This module include the required transformations.
'''
import pickle
from abc import ABC, abstractmethod
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer


class Transformer(ABC):

    @abstractmethod
    def fit(self, *args):
        pass

    @abstractmethod
    def transform(self, *args):
        pass

    @abstractmethod
    def inverse_transform(self, *args):
        pass

    @abstractmethod
    def save(self, address):
        pass

    @classmethod
    @abstractmethod
    def load(cls, address):
        pass


class LabelEncoder(Transformer):
    '''Encode class labels, which severs as a wrapper for sklearn LabelEncoder.
    '''
    def __init__(self):
        self.encoder = preprocessing.LabelEncoder()

    def fit(self, labels):
        '''Fit label encoder.

        A wrapper for fit method of sklearn.preprocessing.LabelEncoder.
        See the sklearn.preprocessing.LabelEncoder.fit method for more
            information.

        '''
        self.encoder.fit(labels)

    def transform(self, labels):
        '''Transform labels to normalized encoding.

        A wrapper for transform method of sklearn.preprocessing.LabelEncoder.
        See the sklearn.preprocessing.LabelEncoder.transform method for more
            information.

        '''
        return self.encoder.transform(labels)

    def inverse_transform(self, encoded_labels):
        '''Transform labels back to original encoding.

        A wrapper for inverse_transform method of sklearn.preprocessing.LabelEncoder.
        See the sklearn.preprocessing.LabelEncoder.inverse_transform method for more
            information.

        '''
        return self.encoder.inverse_transform(encoded_labels)

    def save(self, address):
        '''Write a LabelEncoder to file.

        Args:
            address: Address of the file that the LabelEncoder will be written into.
        '''
        with open(address, 'wb') as fout:
            pickle.dump(self.encoder, fout)

    @classmethod
    def load(cls, address):
        '''Load a LabelEncoder from file.

        Args:
            address: Address of the file that the LabelEncoder will be read from.
        '''
        with open(address, 'rb') as fin:
            return pickle.load(fin)

