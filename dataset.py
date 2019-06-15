'''Create a datasets from valid data files.
'''
import os
import os.path
import pandas as pd


ENCODING = 'utf-8'


class Dataset(object):
    '''An object containing the information about paper abstracts.

    Args:
        paths: A list of files addresses, where each address is the path
            to a valid data file.
        conditions: A list of functions that get a paper represented as a
            dictionary with 'journal', 'title', 'abstract', and 'year'
            s keys.
        sep: A field separator for the files with their address in paths
            parameter. The default is tab ('\t').
    '''
    def __init__(self, paths, conditions, sep='\t'):
        assert isinstance(paths, list), 'paths must be a list of file paths'
        self._data = []
        self.filters = conditions
        for path in paths:
            self.data.extend(Dataset.load(path, conditions, sep=sep))

    @property
    def data(self):
        '''Get abstract information.

        Returns:
            Abstract data as a list of dictionaries.
        '''
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @classmethod
    def load(cls, path, conditions, sep='\t'):
        '''Load abstract data from a given file and filtering it.

        Args:
            path: Address of a valid data file.
            conditions: A list of functions that get a paper represented as a
            dictionary with 'journal', 'title', 'abstract', and 'year' as keys.
            sep: A field separator for the file from the provided path.
                The default is tab ('\t').

        '''
        articles = []
        with open(path, 'r') as fin:
            for line in fin:
                if line.strip() == '':
                    continue
                journal, title, abstract, year = line.strip().split(sep)
                try:
                    year = int(year)
                except ValueError:
                    continue
                paper = {'journal': journal, 'title': title,
                         'abstract': abstract, 'year': year}
                # Apply conditions
                is_valid = True
                for condition in conditions:
                    if condition(paper) is False:
                        is_valid = False
                        break
                if is_valid is True:
                    articles.append(paper)
        return articles

    def to_csv(self, path, sep='\t'):
        '''Write a dataset to file.

        Args:
            path: Address of a valid data file.
            sep: A field separator for the file that dataset will be saved on.
                The default is tab ('\t').
        '''
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'a', encoding=ENCODING) as fout:
            for paper in self.data:
                fout.write('{}{}{}{}{}{}{}\n'.format(paper['journal'], sep,
                                                     paper['title'], sep,
                                                     paper['abstract'], sep,
                                                     paper['year']))

    @classmethod
    def designated_journal(cls, paper, journals):
        '''Check if a paper is from a list of specified journals.

        Args:
            paper: dictionary with 'journal', 'title', 'abstract', and 'year'
                as keys.
            journals: A list of journals.
        Returns:
            True if paper has been published in one of the specified journals.
                False, otherwise.
        '''
        if paper['journal'] in journals:
            return True
        return False

    @classmethod
    def is_in_year_range(cls, paper, year_range):
        '''Check if a paper has been published in a specific range of years.

        Args:
            paper: dictionary with 'journal', 'title', 'abstract', and 'year'
                as keys.
            year_range: A list or tuple of size 2, where
                year_range[0] <= year_range[1].

        Returns:
            True if paper has been published in one of the specified journals.
                False, otherwise.
        '''
        if year_range[0] <= paper['year'] <= year_range[1]:
            return True
        return False

    def to_dataframe(self):
        '''Convert a Dataset object to a pandas DataFrame.

        Returns:
            A pandas.DataFrame that represent the Dataset object.

        '''
        return pd.DataFrame.from_records(self.data,
                                         columns=['journal', 'title',
                                                  'abstract', 'year'])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]
