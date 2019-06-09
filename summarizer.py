'''This module provide data summary for the cleaned PubMed data.

In a terminal run the following command for more information:
python summarizer.py -h
'''
import argparse
import glob
import multiprocessing as mp
from collections import Counter


def summarize(address, sep='\t'):
    '''Get the frequency of papers published per year.

    Args:
        address: A string representing the path to the file containing journal abstracts.
        sep: The field separator in the file containing journal abstracts.

    Returns:
        A Counter object containing journal per year count for each journal.
    '''
    papers = []
    with open(address) as fin:
        for line in fin:
            (journal_name, _, _, year) = line.strip().split(sep)
            try:
                year = int(year)
            except ValueError:
                continue
            papers.append((year, journal_name))
    return Counter(papers)


def main(cleaned_address, out_address, num_proc=1):
    '''Run summarize method for all files in a given directory.

    Args:
        cleaned_address: Address of the directory containing journal abstracts.
        out_address: Address of the file to save data summary into.
        num_proc: A positive integer representing the number of processors to
            be used for summarizing data in parallel.
    '''
    pool = mp.Pool(processes=num_proc)
    results = [pool.apply_async(summarize, args=(address,))
               for address in glob.glob(cleaned_address)]
    summary = Counter()
    for item in results:
        summary += item.get()
    with open(out_address, 'w') as fout:
        fout.write('{}\t{}\t{}\n'.format('Journal', 'Year', 'Count'))
        for (year, journal_name) in sorted(summary.keys(), reverse=True):
            fout.write('{}\t{}\t{}\n'.format(journal_name, year,
                                             summary[(year, journal_name)]))


if __name__ == '__main__':
    parse = argparse.ArgumentParser('python summarizer.py')
    msg = 'Number of processors to use'
    parse.add_argument('-n', '--number_of_processors', type=int, default=2,
                       help=msg)
    message = ('A regular expression (string) representing the address of '
               'the cleaned PubMed files to be summarized')
    parse.add_argument('-s', '--source_files', type=str, required=True,
                       help=message)
    message = 'Address of the file to hold data summary information'
    parse.add_argument('-o', '--output_file', type=str, required=True,
                       help=message)
    arguments = parse.parse_args()

    main(cleaned_address=arguments.source_files,
         out_address=arguments.output_file,
         num_proc=arguments.number_of_processors)
