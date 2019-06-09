'''Generate the address to the PubMed abstract repositories.
Each repository includes information about a collection of
papers in a compressed format. This module generates the links to
PubMed abstracts repositories from ftp://ftp.ncbi.nlm.nih.gov/pubmed
    The files are available from two addresses: One for an annual baseline
and another for daily updates.

Note:
    Baseline and Update information may change annually.

For more information run the following command in a terminal
python downloader.py -h
'''

import time
import logging
import argparse
import os.path
from ftplib import FTP




def extract_links(ftp_path, start_idx, end_idx, name_template):
    ''' Generate file paths on the NCBI FTP server.

    Args:
        ftp_path (str): Directory address where files reside on the FTP server.

        start_idx (int): A number representing the index used to name the first
            file on a specific path on a FTP server. Ascending numerical order
            is used to specify the first file.

        end_idx (int): A number representing the index used to name the first
            file on a specific path on the FTP server. Ascending numerical order
            is used to specify the first file.

        name_template (str): An template used for generating links. "format"
            method is used for generating names using name_template. The only
            place holder in name_template uses integer indices from start_idx to
            end_idx (both inclusive) to generate links.

    Returns:
        links (list): A list of paths to the fils on the PubMed NCBI server.

    '''
    links = []
    for i in range(start_idx, end_idx + 1):
        links.append(os.path.join(ftp_path, name_template.format(i)))
    return links


def to_file(out_address, links):
    ''' Write links to a file.

    Args:
        out_address (str): A file address to write the extracted links to it.

        links (list): A list of file addresses on a FTP server.

    '''
    with open(out_address, 'w') as fout:
        for link in links:
            fout.write('{}\n'.format(link))


def ftp_downloader(server_address, links, local_dir_address, ftp_dir,
                   seconds=2):
    ''' Download files from NCBI FTP server.

    '''
    with FTP(server_address) as ftp:
        ftp.login()
        ftp.cwd(ftp_dir)
        for link in links:
            time.sleep(seconds)
            path = os.path.dirname(link)
            name = os.path.basename(link)
            logger.info(os.path.join(path, name))
            with open(os.path.join(local_dir_address, name), 'bw') as fin:
                ftp.retrbinary('RETR ' + name, fin.write)


def read_links(link_file_address):
    '''Read links from a text file.

    Args:
        link_file_address: A string representing a file address containing links.
            Each line contins the link to a file.
    Returns:
        A list of links to files to be downloaded.
    '''
    links = []
    with open(link_file_address, 'r') as fin:
        for line in fin:
            line = line.strip()
            if line == '':
                continue
            links.append(line)
    return links



if __name__ == '__main__':
    # Setting up a logger
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # Define a parser for parsing command line arguments
    parse = argparse.ArgumentParser('Pubmed Data Extractor.')
    msg = 'yes (or y) if you would like to generate the link files'
    parse.add_argument('-g', '--generate_links', type=str, required=True, help=msg)
    msg = 'yes (or y) if you would like to download the files'
    parse.add_argument('-d', '--download', type=str, required=True, help=msg)
    msg = 'Sleep time between each file download; default 2 second'
    parse.add_argument('-s', '--sleep', type=int, default=2, help=msg)
    args = parse.parse_args()
    SERVER_ADDRESS = 'ftp.ncbi.nlm.nih.gov'
    # See ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline to determine the values for
    # the following variables
    baseline_path = 'pubmed/baseline/'
    baseline_start_idx = 1
    baseline_end_idx = 972

    # See ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/ to determine the values
    # for the following variables
    update_file_path = 'pubmed/updatefiles/'
    update_start_idx = 973
    update_end_idx = 1196
    name_temp = 'pubmed19n{:04d}.xml.gz'

    baseline_link_file_address = 'data/baseline_links.txt'
    daily_update_link_file_address = 'data/daily_update_links.txt'

    if args.generate_links.lower() in {'true', 'yes', 't', 'y'}:
        logger.info('Generating links starts ...')
        # Extract and save baseline file paths to a file
        baseline_links = extract_links(ftp_path=baseline_path,
                                       start_idx=baseline_start_idx,
                                       end_idx=baseline_end_idx,
                                       name_template=name_temp)
        to_file(out_address=baseline_link_file_address, links=baseline_links)

        # Extract and save daily update paths to a file
        daily_update_links = extract_links(ftp_path=update_file_path,
                                           start_idx=update_start_idx,
                                           end_idx=update_end_idx,
                                           name_template=name_temp)
        to_file(out_address=daily_update_link_file_address,
                links=daily_update_links)
        logger.info('Generating links ends successfully.')

    if args.download.lower() in {'true', 'yes', 't', 'y'}:
        sleep = args.sleep
        logging.info("Start downloading files ...")
        out_dir = 'data/raw'

        # Download the baseline files
        baseline_links = read_links(baseline_link_file_address)
        ftp_downloader(SERVER_ADDRESS, baseline_links, out_dir,
                       ftp_dir=baseline_path, seconds=sleep)

        # Download the daily update files
        daily_update_links = read_links(daily_update_link_file_address)
        ftp_downloader(SERVER_ADDRESS, daily_update_links, out_dir,
                       ftp_dir=update_file_path, seconds=sleep)
        logger.info('Downloading files ends successfully.')
