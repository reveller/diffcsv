import csv
import pprint
from collections import namedtuple
import argparse
import sys

dict1 = {}
dict2 = {}


def parse_file(fname, keyfield):
    destdict = {}
    with open(fname, "rt") as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        kfieldnum = headers.index(keyfield)
        # import pdb; pdb.set_trace()
        for row in reader:
            destdict[row[kfieldnum]] = {key: value for key, value in zip(headers, row)}
    # pprint.pprint(destdict)
    return destdict

def compare_dicts(source_file, src_dict, test_file, test_dict):
    for key in src_dict:
        # print("Comparing {}".format(key))
        if test_dict.get(key) is None:
            print("{} exists in {}, but does NOT exist in {}!".format(key, source_file, test_file))

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key-field', help='Field name of the column to use as the key',
                  dest='keyField', type=str)
parser.add_argument('-s', '--source-file', help='Filename of the Source of Authority',
                  dest='sourceFile', type=str)
parser.add_argument('-t', '--test-file', help='Filename of the file to be compared to the source file',
                  dest='testFile', type=str)

parser.add_argument('-n', '--table-name', help='Name of the DynamoDB table to store inventory',
                  dest='tableName', type=str)
parser.add_argument('-p', '--platform', help='Platform name of the OS, stored in the inventory DB',
                  dest='platform', type=str)
parser.add_argument('-r', '--regions', help="A comma separated list of regions",
                  dest='regions', type=str)
                  # dest='regions', type=lambda x: x.split(','))
args = parser.parse_args()

def main():
    # with open("test1.csv") as f:
    #     reader = csv.DictReader(f)
    #     data1 = [r for r in reader]
    # pprint.pprint(data1)
    # data1[0]["first"]

    # with open("test1.csv") as f:
    #     reader = csv.reader(f)
    #     Data = namedtuple("Data", next(reader))
    #     data2 = [Data(*r) for r in reader]
    # pprint.pprint(data2)
    # print(data2[0].first)
    
    # import pdb; pdb.set_trace()

    if args.keyField:
        keyfield = args.keyField
    else:
        print("You gotta tell me where to get the unique key field from!  Try -f")
        sys.exit(1)

    if args.sourceFile is None:
        print("You gotta tell me which source file to get the unique key field from!  Try -s")
        sys.exit(1)

    if args.testFile is None:
        print("You gotta tell me which filename to compare the unique key field against!  Try -t")
        sys.exit(1)

    src_dict = parse_file(args.sourceFile, args.keyField)
    test_dict = parse_file(args.testFile, args.keyField)

    compare_dicts(args.sourceFile, src_dict, args.testFile, test_dict)
    compare_dicts(args.testFile, test_dict, args.sourceFile, src_dict)

if(__name__ == "__main__"):
    main()
