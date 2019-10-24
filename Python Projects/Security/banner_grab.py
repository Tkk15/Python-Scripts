'''
Python Security Toolkit
Banner Grabber
http://www.sourceforge.net/p/pythonsecuritytoolkit

This program is written in Python 3.  Please run it with a Python 3 interpreter.

Python Security Toolkit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Python Security Toolkit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import socket
import time
import argparse
import os.path
import sys



def try_connect_tcp(host,port,file_wr):
    '''
    ***********************************************************************
    * Method name:    try_connect_tcp
    * Method purpose: To connect to port using TCP and retrieve banner data
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     String, Integer, File Object
    * Return:         Void
    ***********************************************************************
    '''
    try:
        try_conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try_conn_tcp.connect((host,port))
        try_conn_tcp.send(b'Hellooooooooo?\r\n')
        result = try_conn_tcp.recv(1024)
        result = str(result)
        port_open = 'TCP port ' + str(port) + ' for ' + host + ' is open.'
        print(port_open)
        print(result)
        try_conn_tcp.shutdown(socket.SHUT_RDWR)
        try_conn_tcp.close()
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(port_open + '\n')
                output_file.write(result + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')
    except:
        port_closed = 'TCP port ' + str(port) + ' for ' + host + ' is closed.'
        print(port_closed)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(port_closed + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')



def try_connect_udp(host,port,file_wr):
    '''
    ***********************************************************************
    * Method name:    try_connect_udp
    * Method purpose: To connect to port using UDP and retrieve banner data
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     String, Integer, File Object
    * Return:         Void
    ***********************************************************************
    '''
    try:
        try_conn_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try_conn_udp.connect((host,port))
        try_conn_udp.send(b'Hellooooooooo?\r\n')
        result = try_conn_udp.recv(1024)
        result = str(result)
        port_open = 'UDP port ' + str(port) + ' for ' + host + ' is open.'
        print(port_open)
        print(result)
        try_conn_udp.shutdown(socket.SHUT_RDWR)
        try_conn_udp.close()
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(port_open + '\n')
                output_file.write(result + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')
    except:
        port_closed = 'UDP port ' + str(port) + ' for ' + host + ' is closed.'
        print(port_closed)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(port_closed + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')



def translate(host,file_wr):
    '''
    ***********************************************************************
    * Method name:    translate
    * Method purpose: To translate the host to an IP address
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     String, File Object
    * Return:         Void
    ***********************************************************************
    '''
    try:
        host_ip = socket.gethostbyname(host)
        result_ip = 'IP address for ' + host + ' is ' + host_ip
        print(result_ip)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(result_ip + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')
    except:
        result_ip_error = "Error! Cannot resolve IP address for " + host
        print(result_ip_error)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(result_ip_error + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')
        return
    try:
        host_name = socket.gethostbyaddr(host_ip)
        host_name = host_name[0]
        result_host_name = 'Hostname for ' + host + ' is ' + host_name
        print(result_host_name)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(result_host_name + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')
    except:
        error_host_name = 'Cannot resolve hostname for ' + host
        print(error_host_name)
        if (file_wr != None):
            try:
                output_file = open(file_wr, 'a')
                output_file.write(error_host_name + '\n')
                output_file.close()
            except:
                print('Error! Cannot save data to file.')



def parse_port_list(port_list):
    '''
    ***********************************************************************
    * Method name:    parse_port_list
    * Method purpose: To convert the list of ports given as command line
    *   arguments into integers.
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     String
    * Return:         List of Integers
    ***********************************************************************
    '''
    portlist = ''
    for port in port_list:
        portlist = portlist + port
    port_list = portlist.split(',')
    for index, port in enumerate(port_list):
        try:
            port_list[index] = int(port)
        except:
            print('Error! Invalid input for port given.')
            sys.exit(0)
    return port_list



def parse_port_range(port_range):
    '''
    ***********************************************************************
    * Method name:    parse_port_range
    * Method purpose: To convert the range of ports given as command line
    *   arguments into a list of integers.
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     String
    * Return:         List of Integers
    ***********************************************************************
    '''
    port_list = []
    for index, port in enumerate(port_range):
        if (',' in port):
            port_range[index] = port.replace(',','')
    for index, port in enumerate(port_range):
        try:
            port_range[index] = int(port)
        except:
            print('Error! Invalid input for port given.')
            sys.exit(0)
    begin_port_range = port_range[0]
    end_port_range = (port_range[1] + 1)
    if (begin_port_range > end_port_range):
        print('Please enter the lower limit port first, then the upper limit port second.')
        print('Example: console>python port_scanner.pyc host-to-scan.com -r 1, 10')
        sys.exit(0)
    else:
        for i in range(begin_port_range,end_port_range):
            port_list.append(i)
    return port_list



def default_ports():
    '''
    ***********************************************************************
    * Method name:    default_ports
    * Method purpose: To create a default list of integers to be used as
    *   ports to be scanned
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     None
    * Return:         List of Integers
    ***********************************************************************
    '''
    port_list = []
    for i in range(1025):
        port_list.append(i)
    return port_list



def file_name(file_w):
    '''
    ***********************************************************************
    * Method name:    file_name
    * Method purpose: To confirm if the user wishes to overwrite file
    *   if it already exists and to create output file.
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     File Object
    * Return:         String
    ***********************************************************************
    '''
    loop_var = True
    while loop_var:
        answer = input(file_w + ' already exists. Do you want to overwrite file? Enter yes or no: ')
        answer = answer.lower()
        if (answer[0] == 'y'):
            output_file = open(file_w, 'w')
            output_file.close()
            file_nm = file_w
            loop_var = False
        elif (answer[0] == 'n'):
            new_file = input('Please enter new filename: ')
            if (new_file != file_w):
                output_file = open(new_file, 'w')
                output_file.close()
                file_nm = new_file
                loop_var = False
    return file_nm



def total_time(start,file_wr):
    '''
    ***********************************************************************
    * Method name:    total_time
    * Method purpose: To calculate and output the run time of the program.
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     Integer, File Object
    * Return:         Void
    ***********************************************************************
    '''
    end_time = time.time()
    total = end_time - start
    total = str(total)
    scan_time = 'Scan took ' + total + ' seconds  to complete.'
    print(scan_time)
    if (file_wr != None):
        try:
            output_file = open(file_wr, 'a')
            output_file.write(scan_time + '\n')
            output_file.close()
        except:
            print('Error! Cannot save data to file.')



def main():
    '''
    ***********************************************************************
    * Method name:    main
    * Method purpose: To parse command line arguments, and call functions
    *   based upon user input.
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Void
    ***********************************************************************
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs=1, help='address of host to be scanned')
    parser.add_argument('-l', '--list', nargs='*', help='comma delimited list of ports to be scanned, ex: -l 20, 21, 22, 80 (ports 1 - 1024 are default.)')
    parser.add_argument('-r', '--range', nargs=2, help='comma delimited inclusive range of ports to be scanned, ex: -r 1, 50 (ports 1 - 1024 are default.)')
    parser.add_argument('-p', '--protocol', nargs=1, help='choose protocol you wish to use. enter t for tcp, u for udp, tu for both. (tcp is default.)')
    parser.add_argument('-w', '--write', nargs=1, help='choose to write output to a file. ex: -w filename')
    args = parser.parse_args()
    start_time = time.time()
    print('\n'*75)
    print('\nPython Security Toolkit')
    print('Banner Grabber')
    input('\nPress enter to continue.')
    target_host = args.host
    target_host = target_host[0]
    if (',' in target_host):
        target_host = target_host.replace(',','')
    file_write = args.write
    if (file_write != None):
        file_write = file_write[0]
        file_exists = os.path.exists(file_write)
        if (file_exists):
            file_write = file_name(file_write)
        else:
            output_file = open(file_write, 'w')
            output_file.close()
    target_protocol = args.protocol
    if (target_protocol != None):
        target_protocol = target_protocol[0]
        if (target_protocol == 't'):
            translate(target_host,file_write)
            target_ports_list = args.list
            if (target_ports_list != None):
                target_ports_list = parse_port_list(target_ports_list)
                for port in target_ports_list:
                    try_connect_tcp(target_host,port,file_write)
                total_time(start_time,file_write)
            target_ports_range = args.range
            if (target_ports_range != None):
                target_ports_range = parse_port_range(target_ports_range)
                for port in target_ports_list:
                    try_connect_tcp(target_host,port,file_write)
                total_time(start_time,file_write)
            if ((target_ports_list == None) and (target_ports_range == None)):
                default_port_list = default_ports()
                for port in default_port_list:
                    try_connect_tcp(target_host,port,file_write)
                total_time(start_time,file_write)
        elif (target_protocol == 'u'):
            translate(target_host,file_write)
            target_ports_list = args.list
            if (target_ports_list != None):
                target_ports_list = parse_port_list(target_ports_list)
                for port in target_ports_list:
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
            target_ports_range = args.range
            if (target_ports_range != None):
                target_ports_range = parse_port_range(target_ports_range)
                for port in target_ports_list:
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
            if ((target_ports_list == None) and (target_ports_range == None)):
                default_port_list = default_ports()
                for port in default_port_list:
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
        elif (target_protocol == 'tu'):
            translate(target_host,file_write)
            target_ports_list = args.list
            if (target_ports_list != None):
                target_ports_list = parse_port_list(target_ports_list)
                for port in target_ports_list:
                    try_connect_tcp(target_host,port,file_write)
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
            target_ports_range = args.range
            if (target_ports_range != None):
                target_ports_range = parse_port_range(target_ports_range)
                for port in target_ports_list:
                    try_connect_tcp(target_host,port,file_write)
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
            if ((target_ports_list == None) and (target_ports_range == None)):
                default_port_list = default_ports()
                for port in default_port_list:
                    try_connect_tcp(target_host,port,file_write)
                    try_connect_udp(target_host,port,file_write)
                total_time(start_time,file_write)
        else:
            print('Error! Please enter -p t for TCP, -p u for UDP, -p tu for both TCP and UDP.  If no selection is made TCP scan is default.')
            sys.exit(0)
    else:
        translate(target_host,file_write)
        target_ports_list = args.list
        if (target_ports_list != None):
            target_ports_list = parse_port_list(target_ports_list)
            for port in target_ports_list:
                try_connect_tcp(target_host,port,file_write)
            total_time(start_time,file_write)
        target_ports_range = args.range
        if (target_ports_range != None):
            target_ports_range = parse_port_range(target_ports_range)
            for port in target_ports_range:
                try_connect_tcp(target_host,port,file_write)
            total_time(start_time,file_write)
        if ((target_ports_list == None) and (target_ports_range == None)):
            default_port_list = default_ports()
            for port in default_port_list:
                try_connect_tcp(target_host,port,file_write)
            total_time(start_time,file_write)



if (__name__ == '__main__'):
    main()
