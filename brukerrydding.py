#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Script for å hente ut navn og affiliations basert på en liste med brukernavn.
# Output er en cvs-fil som kan åpnes i Excel. Husk å spesifisere UTF-8 på input i Excel.

import bofh, pprint, getpass, sys, getopt, codecs

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:o:',['inputfile=','outputfile='])
    except getopt.GetoptError:
        print sys.argv[0] + ' -i <inputfile> -o <outputfile.csv>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0] + ' -i <inputfile> -o <outputfile.csv>'
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    if (outputfile == ''):
        print 'Gi en fil å skrive til, med opsjon -o'
        sys.exit()

    conn = bofh.connect('https://cerebrum-uio.uio.no:8000', 'data/ca.pem') #kobler til cerebrum
    sid = conn._run_raw_command('login', getpass.getuser(), getpass.getpass()) #ber om passord
    conn._session = sid #session id

    brukerrapport = codecs.open(outputfile, encoding='utf-8', mode='w')
    for user in read_userlist(inputfile):
        brukerrapport.write(get_aff(conn, user) + '\n')
    brukerrapport.close()    

def read_userlist(file):
    with open(file, 'r') as f:
        userlist = f.read().splitlines()
    return userlist

def get_aff(conn, user):

    try:
        dict = conn.run_command('person_info', user)
    except bofh.proto.BofhError:
        return user + ' *** Unknown account ***' 
    info = user

    #print user #dersom man ønsker å liste brukernavnene etterhvert som de blir prossesert
    for item in dict:
        if item.has_key('name'):
            info += ',' + item['name'].replace(' [from Cached]', '')
        if item.has_key('affiliation_1'):
            info += ',' + item['affiliation_1']
        if item.has_key('affiliation'):
            info += ',' + item['affiliation']
    return info

if __name__ == "__main__":
    main(sys.argv[1:])
