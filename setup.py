import argparse
import os

parser = argparse.ArgumentParser(description='Setup script for the repo')
parser.add_argument('--quandl_api_key', '-q',
                    dest='quandl_api_key',
                    metavar='<API KEY>',
                    type=str,
                    help='API Key to access Quandl data')

args = parser.parse_args()

print(args.quandl_api_key)
