import unittest
import pandas as pd
from dataset import Dataset
from build_dataset import make_dataset


ENCODING = 'utf-8'


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.address = 'data/processed/PubMedSampleFile.tsv'
        conditions = []
        self.dataset = Dataset([self.address], conditions, sep='\t')
        self.data = pd.read_csv(self.address, sep='\t', header=None,
                                names=['journal', 'title', 'abstract', 'year'])

    def test_dataset_creation(self):
        self.assertTrue(self.dataset is not None)
        for i, paper in enumerate(self.data.itertuples()):
            self.assertEqual(paper.journal, self.dataset[i]['journal'])
            self.assertEqual(paper.abstract, self.dataset[i]['abstract'])
            self.assertEqual(paper.title, self.dataset[i]['title'])
            self.assertEqual(paper.year, self.dataset[i]['year'])

    def test__len__(self):
        self.assertEqual(len(self.dataset), self.data.shape[0])

    def test_to_dataframe(self):
        self.assertTrue(self.data.equals(self.dataset.to_dataframe()))

    def test_to_csv(self):
        address = 'temp/dataset.tmp'
        self.dataset.to_csv(address, sep='\t')
        with open(address, encoding=ENCODING) as fin:
            observed = fin.read()
        with open(self.address, encoding=ENCODING) as fin:
            expected = fin.read()
        self.assertEqual(expected, observed)

    def test_make_dataset(self):
        journals_path = 'data/journals.txt'
        inputs_path = 'data/data_file_addresses.txt'
        earliest = 2000
        latest = 2018
        ds = make_dataset(journals_path, inputs_path, earliest, latest)
        expected_papers = self.data.loc[self.data['journal']=='Ecology', :]
        for i, paper in enumerate(expected_papers.itertuples()):
            self.assertEqual(paper.journal, ds[i]['journal'])
            self.assertEqual(paper.abstract, ds[i]['abstract'])
            self.assertEqual(paper.title, ds[i]['title'])
            self.assertEqual(paper.year, ds[i]['year'])
