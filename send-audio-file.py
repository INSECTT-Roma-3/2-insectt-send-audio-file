#!/usr/bin/env python

#come usarlo: python3 main.py --host 192.168.2.66 --port 21 --user media3tech --password clastemas --path ../INSECTT/

"""Upload either a file or all files in a directory to ftp server."""

import argparse
import logging
import os

from ftplib import FTP_TLS

logging.getLogger().setLevel(logging.DEBUG)


def main(args):
    ftps = FTP_TLS()
    ftps.connect(args.host, args.port)
    logging.debug('Connected')
    ftps.login(args.user, args.password)
    logging.debug('Logged in')
    ftps.prot_p()

    # Note: this assumes that all files in the given directory should be uploaded
    if os.path.isdir(args.path):
        upload_directory(ftps, args.path, args.ftppath)
    elif os.path.isfile(args.path, args.ftppath):
        upload_file(ftps, args.path,  args.ftppath)

    ftps.quit()
    logging.debug('Connection closed')


def upload_directory(ftps, path, ftppath):
    """Upload all files in a given directory.
    :param path: Path to the directory that contains files to upload.
    :type path: str
    """
    chdir(ftps, ftppath)

    
    basenames = os.listdir(args.path)
    for i, basename in enumerate(basenames):
        fname = os.path.join(args.path, basename)
        with open(fname, 'rb') as fp:
            logging.debug(
                '(%d/%d) Uploading file: %s',
                i + 1,
                len(basenames),
                fname,
            )
            ftps.storbinary('STOR {}'.format(basename), fp)
                       
           


def upload_file(ftps, path, ftppath):
    """Upload file to ftp server.
    :param path: Path to the file to be uploaded.
    :type path: str
    """
    chdir(ftps, path)
    
    logging.debug('Uploading file: %s', args.path)
    basename = os.path.basename(args.path)
    with open(args.path, 'rb') as fp:
        ftps.storbinary('STOR {}'.format(basename), fp)
        
# Change directories - create if it doesn't exist
def chdir(ftps, dir): 
    print('cazzo')
    if dir in ftps.nlst() : #check if 'foo' exist inside 'www'
        print ('Directory in ftp exist')
        ftps.cwd(dir)  # change into "foo" directory
        ftps.retrlines('LIST') #list directory contents

    else : 
        print ('Create directory on ftp')
        ftps.mkd(dir) #Create a new directory called foo on the server.
        ftps.cwd(dir) # change into 'foo' directory
        ftps.retrlines('LIST') #list subdirectory contents

# Check if directory exists (in current location)
def directory_exists(ftps, dir):
    filelist = []
    ftps.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='FTP server host (%(default)s by default)',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=21,
        help='FTP server port (%(default)s by default)',
    )
    parser.add_argument('-u', '--user', help='User')
    parser.add_argument('-p', '--password', help='User password')
    parser.add_argument(
        '--path',
        help='Path (either a single file or a directory with files to be uploaded)',
    )
    parser.add_argument(
        '--ftppath',
        help='Path (either a single file or a directory with files to be uploaded)',
    )
    args = parser.parse_args()
    main(args)