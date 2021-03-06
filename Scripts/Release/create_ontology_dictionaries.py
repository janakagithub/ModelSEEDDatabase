import sys
import os
import json
import datetime
import argparse
#from Bio.ExPASy import Enzyme

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = '', formatter_class = argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--test', '-t',
    action = 'store_true',
    help = 'Use local flat files rather than pulling from external source' )

args = parser.parse_args()

## FUNCTIONS ###################################################################

def get_KEGG_KOs():
    kegg_dict = {}

    kegg_api_release = 'curl -g -s -S http://rest.kegg.jp/info/kegg'
    kegg_release_raw = os.popen(kegg_api_release).read()
    kegg_release = kegg_release_raw.split("\n")[1].split()[2]

    kegg_dict = {'data_version'  : kegg_release,
                'date'           : timestamp,
                'format_version' : 'N/A',
                'ontology'       : 'kegg_orthology'
                }

    kegg_raw = ""

    if args.test == False:
        kegg_api_call = 'curl -g -s -S http://rest.kegg.jp/list/orthology'
        kegg_raw = os.popen(kegg_api_call).read()
    else:
        with open('kegg_orthologs.txt', 'r') as myfile:
            kegg_raw = myfile.read()

    kegg_dict['term_hash'] = {}

    for line in kegg_raw.split("\n"):

        if len(line) > 0:

            id, name_raw = line.split("\t")
            id = id.replace("ko:", "")

            nameSplit = name_raw.split(";")

            name = ""
            synonym = ""

            if len(nameSplit) > 1:
                name = nameSplit[1].strip()
                synonym = nameSplit[0].strip()
            else:
                print(name)

            kegg_dict['term_hash'][id] = {'id' : id, 'name' : name, 'synonyms' : synonym.split(", ")}

    with open('../../Ontologies/KBaseOntology.OntologyDictionary.KEGG_KO_ontologyDictionary.json', 'w') as outfile:
        json.dump(kegg_dict, outfile, indent = 2)

def get_KEGG_RXNs():
    kegg_dict = {}

    kegg_api_release = 'curl -g -s -S http://rest.kegg.jp/info/kegg'
    kegg_release_raw = os.popen(kegg_api_release).read()
    kegg_release = kegg_release_raw.split("\n")[1].split()[2]

    kegg_dict = {'data_version'  : kegg_release,
                'date'           : timestamp,
                'format_version' : 'N/A',
                'ontology'       : 'kegg_orthology'
                }

    kegg_raw = ""

    if args.test == False:
        kegg_api_call = 'curl -g -s -S http://rest.kegg.jp/list/reaction'
        kegg_raw = os.popen(kegg_api_call).read()
    else:
        with open('kegg_reactions.txt', 'r') as myfile:
            kegg_raw = myfile.read()

    kegg_dict['term_hash'] = {}

    for line in kegg_raw.split("\n"):

        if len(line) > 0:

            id, name_raw = line.split("\t")
            id = id.replace("rn:", "")

            fullLineSplit = name_raw.split("; ")

            name = fullLineSplit.pop(0)

            kegg_dict['term_hash'][id] = {'id' : id, 'name' : name, 'synonyms' : fullLineSplit}

    with open('../../Ontologies/KBaseOntology.OntologyDictionary.KEGG_RXN_ontologyDictionary.json', 'w') as outfile:
        json.dump(kegg_dict, outfile, indent = 2)

def get_EC_RXNs():
    ec_dict = {}

    # version
    ebi_ec_release = ""

    if args.test == False:
        ebi_ec_call = 'curl ftp://ftp.ebi.ac.uk/pub/databases/enzyme/enzclass.txt'
        ebi_ec_release = os.popen(ebi_ec_call).read()
    else:
        with open('enzclass.txt', 'r') as myfile:
            ebi_ec_release = myfile.read()

    ebi_ec_release = ebi_ec_release.split("\n")[7].split()[1]

    ec_dict = {'data_version'    : ebi_ec_release,
                'date'           : timestamp,
                'format_version' : 'N/A',
                'ontology'       : 'ec_orthology'
                }

    # parser

    ebi_ec_enzyme = 'enzyme.dat'

    if args.test == False:
        ebi_ec_call = 'curl ftp://ftp.ebi.ac.uk/pub/databases/enzyme/enzyme.dat > enzyme.dat'
        os.system(ebi_ec_call)

    records = Enzyme.parse(open(ebi_ec_enzyme))
    for record in records:
        ec_dict[record['ID']] = {'id'       : record['ID'],
                                 'name'     : record['DE'],
                                 'synonyms' : record['AN']
                                 }

    with open('../../Ontologies/KBaseOntology.OntologyDictionary.EBI_EC_ontologyDictionary.json', 'w') as outfile:
        json.dump(ec_dict, outfile, indent = 2)

## RUN FUNCTIONS ###############################################################

get_KEGG_KOs()
get_KEGG_RXNs()
#get_EC_RXNs()
