#!/usr/bin/python
# -*- coding: utf-8 -*-
# Script for å sjekke etter ledige IP-adresser på et subnet
#
import bofh, pprint, getpass, sys, getopt

def main(argv):
    subnet = ''
    outputfile = ''
    skjermoutput = False

    try:
        opts, args = getopt.getopt(argv, 'hs:o:',['subnet=','outputfile='])
    except getopt.GetoptError:
        print sys.argv[0] + ' -s <subnet> -o <outputfile.csv>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0] + ' -s <subnet> -o <outputfile.csv>'
            sys.exit()
        elif opt in ('-s', '--subnet'):
            subnet = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    if (outputfile == ''):
        print 'Gi en fil å skrive til, med opsjon -o'
        sys.exit()
    elif (outputfile == 'ledig'):
        skjermoutput = True

    conn = bofh.connect('https://cerebrum-uio.uio.no:8000', 'data/ca.pem') #kobler til cerebrum
    sid = conn._run_raw_command('login', getpass.getuser(), getpass.getpass()) #ber om passord
    conn._session = sid #session id

    #print run_subnet(subnet)

    for host in run_subnet(subnet):
        #print host
        try:
            print get_hostinfo(conn, host) + '\n'
        except:
            print 'ping pong'

    """
    if not skjermoutput:
        dhcprapport = open(outputfile, mode='w')
        for host in run_subnet(subnet):
            dhcprapport.write(get_hostinfo(conn, host) + '\n')
        dhcprapport.close()    
    """

def run_subnet(subnet):

    double = True
    if (subnet == '79'):
        double = False
    elif (subnet == '159'):
        double = False
    elif (subnet == '132'):
        double = False
    
    subnetlist = [] 
    for i in range(150,180):
        subnetlist.append('129.240.' + subnet + '.' + str(i))
    if double:
        subnet = int(subnet) + 1
        for i in range(12,25):
            subnetlist.append('129.240.' + str(subnet) + '.' + str(i))

    print subnetlist
    return subnetlist

def get_hostinfo(conn, host):

    dict = conn.run_command('host_info', host)
    info = host

    print host #dersom man ønsker å liste brukernavnene etterhvert som de blir prossesert
    for item in dict:
        if item.has_key('name'):
            print item['name']
            info += ',' + item['name'].replace('.uio.no.', '')
        if item.has_key('mac'):
            if (item['mac'] == None):
                info += ',None'
            else:
                info += ',' + item['mac']
    return info

if __name__ == "__main__":
    main(sys.argv[1:])
