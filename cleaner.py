'''This module extract features from the raw compressed files.

Raw data obtained from PubMed. For information about using
this module run the following command.

python cleaner.py -h
'''

import argparse
import re
import glob
import gzip
import os
import os.path
import multiprocessing as mp
import logging
from collections import Counter
from bs4 import BeautifulSoup



class Error(Exception):
    'Base class for exceptions in this module.'


class LanguageNotSupportedError(Error):
    'Exception to be raised when a language is not supported.'



class AbstractNotAvailableError(Error):
    'Exception to be raised when abstract is not available.'


class PublicationYearMissingError(Error):
    'Exception to be raised when publication is not available.'



def get_article_data(article):
    '''Extract features from an article tag from the PubMed XML files.

    Args:
        article: An string representing an article tag for PubMed data.

    Returns:
        A dictionary of extracted features, such as Title, Abstract,
            JournalName, and PubYear (publication year).

    '''
    language = article.Article.Language.text
    if language not in {'eng', 'Eng', 'english', 'English'}:
        raise LanguageNotSupportedError(('{} is not a supported ' +
                                         'language!').format(language))
    paper = dict()
    # get journal name
    journal_name = article.Article.Journal.Title.text
    journal_name = re.sub('[\t\n\r]+', ' ', journal_name).strip()
    paper['JournalName'] = journal_name.strip()
    # get paper publish year
    try:
        pub_date = article.Article.JournalIssue.PubDate
        year = re.split('[ \t -]', pub_date.MedlineDate.text)[0].strip()
    except AttributeError as e:
        try:
            year_season_info = pub_date.Year.text.split()
            valid_year = False
            for val in year_season_info:
                if(val.isdigit() and len(val) == 4):
                    valid_year = True
                    year = val
                    break
            if valid_year is False:
                raise PublicationYearMissingError('Cannot find publication year')
        except AttributeError as e:
            raise PublicationYearMissingError('Cannot find publication year')
    paper['PubYear'] = year
    # get paper title
    paper_title = article.Article.ArticleTitle.text
    paper_title = re.sub('[\t\n\r]+', ' ', paper_title).strip()
    paper['Title'] = paper_title
    # get abstract
    abstract = article.Article.Abstract
    if (abstract is None) or (abstract.AbstractText is None):
        raise AbstractNotAvailableError('Abstract is not Available')
    abstract = re.sub('[\t\n\r]+', ' ',
                      abstract.AbstractText.text).strip()
    paper['Abstract'] = abstract
    return paper


def get_content(input_address, output_address):
    '''Clean all .gz file save the resulted clean file.

    Args:
        input_address: Address of a .gz file from PubMed.
        output_address: Address of a the generated cleaned file.

    Returns:
        A dictionary representing the number of cleaned abstracts
            (#Abstracts) and the number of processed records (#Records).

    '''
    data = list()
    with gzip.open(input_address, mode='rt', encoding='utf-8') as fin:
        contents = fin.read()
        soup = BeautifulSoup(contents, 'xml')
        del contents
        articles = soup.find_all('PubmedArticle')
        del soup
        languages = set()
        num_records = 0
        num_cleand_abs = 0
        for article in articles:
            try:
                num_records += 1
                paper_info = get_article_data(article)
                data.append(paper_info)
                num_cleand_abs += 1
            except LanguageNotSupportedError as e:
                continue
            except AbstractNotAvailableError as e:
                continue
            except PublicationYearMissingError as e:
                continue
        with open(output_address, mode='w', encoding='utf-8') as fout:
            for paper in data:
                fout.write('{}\t{}\t{}\t{}\n'.format(paper['JournalName'],
                                                     paper['Title'],
                                                     paper['Abstract'],
                                                     paper['PubYear']))
        result = {'#Abstracts':num_cleand_abs,
                  '#Records': num_records}
        return(result)


def parallel_cleaner(source_dir, output_dir, number_of_processors, logger):
    '''Cleans file in parallel.

    This method cleans all of the provided .gz files and saves the
        cleaned files containing the features as a tab-separated files.

    Args:
        source_dir: Address of the directory containing .gz files
            extracted from PubMed.
        output_dir: Address of the directory to save the processed files.
        number_of_processors: Number of processor used for data cleaning.
        logger: A logging object to log the number of processed records
            and the number of cleaned abstracts.

    '''
    pool = mp.Pool(number_of_processors)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    addresses = []
    for name in glob.glob(os.path.join(source_dir, '*.gz')):
        # Remove file extensions and get the base names
        no_extension_name = name[:-7]
        basename = os.path.basename(no_extension_name)
        out_address = os.path.join(output_dir, '{}.tsv'.format(basename))
        addresses.append((name, out_address))
    results = [pool.apply_async(get_content, args=(name, out_address))
               for (name, out_address) in addresses]
    total = Counter()
    for e in results:
        total += Counter(e.get())
    msg = '\t'.join(['{}: {}'.format(key, value)
                    for key, value in total.items()])
    logger.info(msg)


if __name__ == '__main__':
    # Define a parser for parsing command line arguments
    parse = argparse.ArgumentParser('python cleaner.py')
    message = 'The address of the directory containing the raw PubMed .gz files'
    parse.add_argument('-s', '--source_dir', type=str, required=True, help=message)
    message = 'The address of the directory to save the cleaned files'
    parse.add_argument('-o', '--output_dir', type=str, required=True, help=message)
    parse.add_argument('-n', '--number_of_processors', type=int, default=1,
                       help='Number of processors to use')    
    arguments = parse.parse_args()
    # Define a logging object
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    parallel_cleaner(source_dir=arguments.source_dir,
                     output_dir=arguments.output_dir,
                     number_of_processors=arguments.number_of_processors,
                     logger=logger)
