''' This module extracts a dataset from the whole data available.

The data are extracted for a number of journals and for a specific
period of time.

Run the following command in a terminal for more information:
python build_dataset.py -h

'''
import argparse
from dataset import Dataset


def extract_dataset(journals, paths, earliest, latest):
    '''Extract a limited amount of data for specific journals and time-range.

    Args:
        journals: A list of journal names, as represented in PubMed.
        paths: A list of file addresses, where each file address represents the
            address of a valid data file (see Dataset).
        earliest: An integer representing the publication year of the oldest
            journals to be returned.
        latest: An integer representing the publication year of the most
            recent journals to be returned.

    Returns:
        A Dataset object created from all paper abstracts from the specified
            journals and publication years from the files in paths.

    '''

    filters = [lambda paper: Dataset.designated_journal(paper, journals),
               lambda paper: Dataset.is_in_year_range(paper,
                                                      (earliest, latest))]

    dataset = Dataset(paths, filters, sep='\t')
    return dataset


def make_dataset(journals_path, inputs_path, earliest, latest):
    '''Create a dataset of paper abstracts.

    Args:
        journals_path: Address of a file containing journal names one per line.
        inputs_path: Address of the file containing the path to all valid data.
            A valid data file contain journal name, title, abstract, and
            publication year in a tab-separated format.
        earliest: An integer representing the publication year of the oldest
            journals to be returned.
        latest: An integer representing the publication year of the most
            recent journals to be returned.

    Returns:
        A dataset generated from the specified list of journals within the
            specified time frame.
    '''
    #Read journal names from a file
    journals = []
    with open(journals_path, 'r') as fin:
        for line in fin:
            line = line.strip()
            if line == '':
                continue
            journals.append(line)
    #Read data file paths from a file
    paths = []
    with open(inputs_path, 'r') as fin:
        for line in fin:
            line = line.strip()
            if line == '':
                continue
            paths.append(line)
    #Create and return the dataset
    return extract_dataset(journals, paths, earliest, latest)


if __name__ == '__main__':
    # Define a parser for parsing command line arguments
    parse = argparse.ArgumentParser('python build_dataset.py')
    msg_earliest = ('An integer number representing the publication year of the ' +
                    'oldest journals to be returned.')
    parse.add_argument('-e', '--earliest', type=int, required=True,
                       help=msg_earliest)
    msg_latest = ('An integer number representing the publication year of the ' +
                  'most recent journals to be returned.')
    parse.add_argument('-l', '--latest', type=int, required=True, help=msg_latest)
    msg_journals = ('Address of a text file containing the journals of interest. ' +
                    'Each line contains a journal name as represented by PubMed.')
    parse.add_argument('-j', '--journals_path', type=str, required=True,
                       help=msg_journals)
    msg_out_address = 'Address of the file where the extracted dataset is saved.'
    parse.add_argument('-o', '--out_address', type=str, required=True,
                       help=msg_out_address)
    msg_out_address = ('Address of the file containing the address of the ' +
                       'cleaned tabular files.')
    parse.add_argument('-c', '--inputs_path', type=str, required=True,
                       help=msg_out_address)

    args = parse.parse_args()
    ds = make_dataset(args.journals_path, args.inputs_path,
                      args.earliest, args.latest)
    ds.to_csv(args.out_address, sep='\t')
