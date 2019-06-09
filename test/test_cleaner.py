import unittest
import os.path
from bs4 import BeautifulSoup
import logging
import cleaner


class TestCleaner(unittest.TestCase):
    def test_get_article_data(self):
        article_data_path = 'test/sample_data/article_tag.xml'
        article_abstract_file_address = 'test/sample_data/sample_abstract.txt'
        with open(article_data_path, 'r') as fin:
            data = fin.read()
        tag = BeautifulSoup(data, "xml")
        artical = cleaner.get_article_data(tag)
        self.assertEqual(artical['JournalName'], 'Ecology')
        self.assertEqual(artical['PubYear'], '2018')
        title = ('Spatial scale modulates the inference of metacommunity '
                 'assembly processes.')
        self.assertEqual(artical['Title'], title)
        with open(article_abstract_file_address) as fin:
            artical_abstract = fin.read()
        self.assertEqual(artical['Abstract'], artical_abstract)

    def test_parallel_cleaner(self):
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        data_dir = 'test/sample_data/clean_in_parallel_data/'
        expected_path = os.path.join(data_dir, 'output_dir/expected.tsv')
        cleand_file_path = os.path.join(data_dir, 'output_dir/PubMedSampleFile.tsv')
        cleaner.parallel_cleaner(source_dir=os.path.join(data_dir, 'source_dir'),
                                 output_dir=os.path.join(data_dir, 'output_dir'),
                                 number_of_processors=2,
                                 logger=logger)
        with open(expected_path) as fin:
            expected = fin.read()
        with open(cleand_file_path) as fin:
            cleaned = fin.read()

        self.assertEqual(expected, cleaned)





if __name__ == '__main__':
    unittest.main()
