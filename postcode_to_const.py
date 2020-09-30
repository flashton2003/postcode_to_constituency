import os
try:
    import cPickle as pickle
except:
    import pickle
import argparse
'''
Implements a lookup of uk westminster constituency name from post code, using the ONS postcode database and the code history database.
'''
#get the latest ONS postcode database here
#http://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-latest-centroids
#
onspd_file = 'ONSPD.csv'
# get the latest code history database here
#https://ons.maps.arcgis.com/home/search.html?t=content&q=tags%3ACode%20History%20Database&start=1&sortOrder=desc&sortField=modified
# you want the equivilents.csv file
#
chd_file = 'chd.csv'

def parse_onspd(onspd_file):
    """parses onspd file and returns a dict that resolves postcode to constituency code"""
    res_dict = {}
    with open(onspd_file, 'r') as fi:
        for line in fi:
            if not ((line.startswith('p')) & ("live" in line)):
                split_line = line.split(',')
                postcode = split_line[5].strip('"')
                constituencyCode = split_line[10].strip('"')
                res_dict[postcode] = constituencyCode
    with open('.postcode_to_constituencyCode.pick', 'wb') as fo:
        pickle.dump(res_dict, fo, -1)
        print "A!"
    return res_dict

def parse_chd(chd_file):
    """parses the code history database and returns a dict that resolves constitudency code to constitudency name"""
    res_dict = {}
    with open(chd_file) as fi:
        for line in fi:
            if not line.startswith('\"GEOGCD\",\"GEOGNM\"'):#not the key 
                if not line.split(',')[1] == '':#If a line doesn't have a constituency name
                    constituencyCode = line.split(',')[0].strip('"')
                    constituencyName = line.split(',')[1].strip('"')
                    res_dict[constituencyCode] = constituencyName
    with open('.constituencyCode_to_constituencyName.pick', 'wb') as fo:
        print "B!"
        pickle.dump(res_dict, fo, -1)
    return res_dict

def write_lookup(postcode_to_constituencyCode, constituencyCode_to_constituencyName, outputFile):
    """writes a lookup table to an output file"""
    for postcode in postcode_to_constituencyCode:
        try:
            constituencyCode = postcode_to_constituencyCode[postcode] 
            constituencyName = constituencyCode_to_constituencyName[constituencyCode] 
            lineToWrite = postcode + '\t' +constituencyName
            outputFile.write(lineToWrite + "\n")
        except KeyError:
            print "No constituency code for %s" % (postcode)
            continue

def build(outputFilename = "lookup.tsv"):
    global constituencyCode_to_constituency 
    global postcode_to_constituencyCode 
    postcode_to_constituencyCode = parse_onspd(onspd_file)
    constituencyCode_to_constituency = parse_chd(chd_file)
    write_lookup(postcode_to_constituencyCode, constituencyCode_to_constituency,open(outputFilename,"w"))

def load():
    if checkPathsExist():
        global constituencyCode_to_constituency 
        global postcode_to_constituencyCode 
        constituencyCode_to_constituency = pickle.load(open('.constituencyCode_to_constituencyName.pick', 'rb'))
        postcode_to_constituencyCode = pickle.load(open('.postcode_to_constituencyCode.pick', 'rb'))
        return True
    else:
        print "looks like you forgot to build your postcode lists- use -b to build the lookup tables!"
        return False
def checkPathsExist():
    if os.path.exists('.constituencyCode_to_constituencyName.pick') &os.path.exists('.postcode_to_constituencyCode.pick'):
        return True
    return False

def lookup(postcode):
    constituencyCode = postcode_to_constituencyCode[postcode.upper()]
    constituencyName = constituencyCode_to_constituency[constituencyCode]
    return constituencyName

parser = argparse.ArgumentParser(description='builds and uses lookup tables between uk postcodes and uk constituencies')
parser.add_argument("-b",action='store_true', help="builds a new lookup table")
parser.add_argument("-f", help="choses the location of the lookup table(default: lookup.tsv")
parser.add_argument("-l", help="Looks up a postcode(will throw an error if there's no lookup table!)")
args = vars(parser.parse_args())
def main():
    if args["b"]:
        if args["f"]:
            build(args["f"])
        else:
            build()
    else:
        if not load():
            return
    if args["l"]:
        print lookup(args["l"])
main()
