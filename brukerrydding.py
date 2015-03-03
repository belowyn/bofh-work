#!/usr/bin/python

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

    conn = bofh.connect('https://cerebrum-uio.uio.no:8000', 'data/ca.pem') #kobler til cerebrum
    sid = conn._run_raw_command('login', getpass.getuser(), getpass.getpass()) #ber om passord
    conn._session = sid #session id

    brukerrapport = codecs.open(outputfile, encoding='utf-8', mode='w')


    #brukerrapport.write('brukernavn,fullt navn,affiliation(s)\n')
    for user in read_userlist(inputfile):
        brukerrapport.write(get_aff(conn, user) + '\n')

    brukerrapport.close()    

def read_userlist(file):
    with open(file, 'r') as f:
        userlist = f.read().splitlines()
    return userlist


def get_aff(conn, user):

    dict = conn.run_command('person_info', user)
    info = user

    print user
    for item in dict:
        if item.has_key('name'):
            info += ',' + item['name'].replace(' [from Cached]', '')
        if item.has_key('affiliation_1'):
            info += ',' + item['affiliation_1']
            #print item['affiliation_1']
        if item.has_key('affiliation'):
            #print item['affiliation']
            info += ',' + item['affiliation']

    #print info
    return info

if __name__ == "__main__":
    main(sys.argv[1:])

