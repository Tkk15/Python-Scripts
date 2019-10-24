'''
Python Security Toolkit
MAC/NetBios Scanner
http://pythonsecuritytoolkit.sourceforge.net/

This program is written in Python.  Please run it in a Python 3 interpreter.

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



import subprocess
import re
import os
import socket
import sys
import threading
import datetime
import argparse
import signal
import io



class mc_nb_scan():
    '''
    ***********************************************************************
    * Class Name: 	mc_nb_scan
    * Class Purpose:	To hold methods and data associated with an
    *                   instance of the mc_nb_scan class
    * Date created: 	January 19, 2014
    * Last modified: 	January 19, 2014, by: bbishop423
    ***********************************************************************
    '''



    def __init__(self):
        '''
        ***********************************************************************
        * Method name:    __init__
        * Method purpose: To create an instance of the mc_nb_scan class and
        *                 to set the default values for class variables.
        * Date created:   January 19, 2014
        * Last modified:  January 21, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Void
        ***********************************************************************
        '''
        self.host_range = []
        self.begin = 0
        self.end = 0
        self.scan_type = 'mn'
        self.write_logfile = False
        self.log_file = ''
        self.verbose=0
        self.counter=0
        self.lock=threading.Lock()



    def dec2bin(self,n,d=None):
        '''
        ***********************************************************************
        * Method name:    dec2bin
        * Method purpose: To convert Decimal To Binary (Used when input in CIDR Format)
        * Date created:   January 19, 2014
        * Last modified:  January 21, 2014, by: Vincian
        * Parameters:     String                         
        * Return:         String
        ***********************************************************************
        '''
        s = ""
        while n>0:
            if n&1:
                s = "1"+s
            else:
                s = "0"+s
            n >>= 1
        if d is not None:
            while len(s)<d:
                s = "0"+s
        if s == "": s = "0"
        return s



    def bin2ip(self,b):
        '''
        ***********************************************************************
        * Method name:    bin2ip
        * Method purpose: To convert Binary to Decimal (Used when input in CIDR Format)
        * Date created:   January 19, 2014
        * Last modified:  January 19, 2014, by: Vincian
        * Parameters:     String
        * Return:         String
        ***********************************************************************
        '''
        ip = ""
        for i in range(0,len(b),8):
            ip += str(int(b[i:i+8],2))+"."
        return ip[:-1]



    def ip2bin(self,ip):
        '''
        ***********************************************************************
        * Method name:    ip2bin
        * Method purpose: To convert IP Address to Binary Equivalent (Used when input in CIDR Format)
        * Date created:   January 19, 2014
        * Last modified:  January 19, 2014, by: Vincian
        * Parameters:     String
        * Return:         String
        ***********************************************************************
        '''
        b = ""
        inQuads = ip.split(".")
        outQuads = 4
        for q in inQuads:
            if q != "":
                b += self.dec2bin(int(q),8)
                outQuads -= 1
        while outQuads > 0:
            b += "00000000"
            outQuads -= 1
        return b



    def convertCIDRtorange(self,c):
        '''
        ***********************************************************************
        * Method name:    convertCIDRtorange
        * Method purpose: To convert CIDR input to equivalent IP Range (Used when input in CIDR Format)
        * Date created:   January 19, 2014
        * Last modified:  January 21, 2014, by: Vincian
        * Parameters:     String
        * Return:         Void
        ***********************************************************************
        '''
        parts = c.split("/")
        IP = self.ip2bin(parts[0])
        subnet = int(parts[1])
        ipPrefix = IP[:-(32-subnet)]
        self.host_range=[]
        for i in range(2**(32-subnet)):
            if self.bin2ip(ipPrefix+self.dec2bin(i, (32-subnet)))!="192.168.5.0" and self.bin2ip(ipPrefix+self.dec2bin(i, (32-subnet)))!="192.168.5.255":
                self.host_range.append(self.bin2ip(ipPrefix+self.dec2bin(i, (32-subnet))))



    def generate(self):
        '''
        ***********************************************************************
        * Method name:    generate
        * Method purpose: To generate a range of hosts
        * Date created:   January 19, 2014
        * Last modified:  January 19, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Integer
        ***********************************************************************
        '''
        if int(self.host_range[0].split('/')[1])==32:
            self.host_range=[self.host_range[0].split('/')[0]]
            return 1
        else:
            try:
                cidrBlock = self.host_range[0]
                self.convertCIDRtorange(cidrBlock)
            except:
                pass
            return 1



    def valid_ip(self):
        '''
        ***********************************************************************
        * Method name:    valid_ip
        * Method purpose: To check if supplied IP address is valid
        * Date created:   January 19, 2014
        * Last modified:  January 19, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Boolean
        ***********************************************************************
        '''
        ip_valid = False
        try:
            for ip in self.host_range:
                socket.inet_aton(ip)
            ip_valid = True
            return ip_valid
        except:
            print("?? "+ip+" ??")



    def macresolve4nt(self,arg1,arg2):
        '''
        ***********************************************************************
        * Method name:    macresolve4nt
        * Method purpose: To resolve MAC/NetBIOS for Windows systems
        * Date created:   January 19, 2014
        * Last modified:  January 23, 2014, by: bbishop423
        * Parameters:     Integer, Integer
        * Return:         Void
        ***********************************************************************
        '''
        for i in range(arg1,arg2):
            ip=self.host_range[i]
            mac_addr = None
            sys_name = None
            if (self.scan_type == 'm'):
                cmd = 'arp -a ' + ip + '\n'
            elif (self.scan_type == 'n'):
                cmd = 'nbtstat -A ' + ip + '\n'
            else:
                pass
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output, errors = p.communicate()
                output = output.decode('utf-8')
                if (output != None and self.scan_type == 'm'):
                    mac_addr = re.findall('\w\w-\w\w-\w\w-\w\w-\w\w-\w\w',output)
                    mac_addr = str(mac_addr[0])
                    print("["+ ip +"]",end="")
                    for k in range(0,14-len(ip)):
                            print(" ",end="");
                    print(" |  "+str(mac_addr),end="\n")
                    self.lock.acquire()
                    self.counter=self.counter+1
                    self.lock.release()
                    if (self.write_logfile):
                        logfile = open(self.log_file, 'a')
                        logfile.write(results)
                        logfile.close()
                elif (output != None and self.scan_type == 'n'):
                    f = io.StringIO(output)
                    for line in f:
                        if ('<00>' in line and 'UNIQUE' in line):
                            sub = line.find('<')
                            sys_name = line[:sub]
                            sys_name = sys_name.strip()
                        if ('MAC Address' in line):
                            sub = line.find('=')
                            mac_addr = line[(sub+1):]
                            mac_addr = mac_addr.strip()
                    print("["+ ip +"]",end="")
                    for k in range(0,14-len(ip)):
                        print(" ",end="");
                    print(" |  "+str(mac_addr)+"  |  "+str(sys_name),end="\n")
                    self.lock.acquire()
                    self.counter=self.counter+1
                    self.lock.release()
                    if (self.write_logfile):
                        logfile = open(self.log_file, 'a')
                        logfile.write(results2)
                        logfile.close()
            except:
                print("Error Occurred at "+ip,end="\n");



    def macresolve4nix(self,arg1,arg2):
        '''
        ***********************************************************************
        * Method name:    macresolve4nix
        * Method purpose: To resolve MAC/NetBIOS for POSIX systems
        * Date created:   January 19, 2014
        * Last modified:  January 20, 2014, by: Vincian
        * Parameters:     Integer, Integer
        * Return:         Void
        ***********************************************************************
        '''
        for i in range(arg1,arg2):
            ip=self.host_range[i]
            if (self.scan_type == 'n'):
                cmd = 'nmblookup -A ' + ip + ' 2>/dev/null'
            elif (self.scan_type == 'm'):
                cmd = 'arping -f -c 5 ' + ip + ' -I wlan0 2>/dev/null'
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output, errors = p.communicate()
                output = output.decode('utf-8')
                if (output != None):
                    if (self.write_logfile):
                        logfile = open(self.log_file, 'a')
                        logfile.write(output)
                        logfile.close()
                    if self.scan_type=="m":
                        try:
                            mac_addr=re.findall(r'(\[.*\])', output)[0].replace('[', '').replace(']', '')
                            print("["+ ip +"]",end="")
                            for k in range(0,14-len(ip)):
                                print(" ",end="");
                            print(" |  "+str(mac_addr),end="\n")
                            self.lock.acquire()
                            self.counter=self.counter+1
                            self.lock.release()
                        except:
                            if verbose!=0:
                                print("Error Ocurred! [ Host "+str(ip)+" ]",end="\n")                            
                    elif self.scan_type=="n":
                            try:
                                try:
                                    name=re.findall(r'(.*<00>.*)',output)[0]
                                    sys_name=name[0:name.index('<')].replace('\t','')
                                except:
                                    pass
                                mac_addr=re.findall(r'(Address = .*)',output)[0].replace('Address = ','')
                                if(mac_addr=="00-00-00-00-00-00"):
                                    cmd = 'arping -f -c 5 ' + ip + " -I wlan0 2>/dev/null"
                                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                                    output, errors = p.communicate()
                                    output=output.decode('utf-8')
                                    if output is not None :
                                        if (self.write_logfile):
                                            logfile = open(self.log_file, 'a')
                                            logfile.write(output)
                                            logfile.close()
                                        mac_addr=re.findall(r'(\[.*\])', output)[0].replace('[', '').replace(']', '')
                                print("["+ ip +"]",end="")
                                for k in range(0,15-len(ip)):
                                    print(" ",end="");
                                print(" |  "+str(mac_addr)+"  |  "+str(sys_name),end="\n")
                                self.lock.acquire()
                                self.counter=self.counter+1
                                self.lock.release()
                            except:
                                try:
                                    cmd = 'arping -f -c 5 ' + ip + " -I wlan0 2>/dev/null"
                                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                                    output, errors = p.communicate()
                                    output=output.decode('utf-8')
                                    if output is not None :
                                        if (self.write_logfile):
                                            logfile = open(self.log_file, 'a')
                                            logfile.write(output)
                                            logfile.close()
                                        mac_addr=re.findall(r'(\[.*\])', output)[0].replace('[', '').replace(']', '')
                                        print("["+ ip +"]",end="")
                                        for k in range(0,15-len(ip)):
                                            print(" ",end="");
                                        print(" |  "+str(mac_addr)+"  |  (Couldn't Resolve)",end="\n")
                                        self.lock.acquire()
                                        self.counter=self.counter+1
                                        self.lock.release()
                                except:
                                    if self.verbose!=0:
                                        print("Error Ocurred! [ Host "+ip+" ]",end="\n")
            except:
                if self.verbose!=0:
                    print("Error Occurred at "+ip,end="\n");



    def create_range(self,begin,end,prefix):
        '''
        ***********************************************************************
        * Method name:    create_range
        * Method purpose: To create a list of IP addresses within the
        *     specified range
        * Date created:   January 19, 2014
        * Last modified:  January 19, 2014, by: bbishop423
        * Parameters:     Integer, Integer, String
        * Return:         Void
        ***********************************************************************
        '''
        host_range = []
        try:
            for i in range(begin,(end+1)):
                host_range.append(prefix + str(i))
            self.host_range = host_range
            self.begin = begin
            self.end = (end+1)
        except:
            print('Could not resolve IP address.')
            sys.exit(0)



    def create_log(self,file_name):
        '''
        ***********************************************************************
        * Method name:    create_log
        * Method purpose: To create a file to save the scan output to.
        * Date created:   January 21, 2014
        * Last modified:  January 21, 2014, by: bbishop423
        * Parameters:     String
        * Return:         Void
        ***********************************************************************
        '''
        if (os.path.isfile(file_name)):
            while True:
                answer = input(file_name + ' already exists. Do you wish to overwrite it? (y/n): ')
                answer = answer.lower()
                answer = answer[0]
                if (answer == 'y'):
                    logfile = open(file_name, 'w')
                    logfile.close()
                    break
                if (answer == 'n'):
                    file_name2 = input('Please enter a new file name: ')
                    if (file_name == file_name2):
                        continue
                    else:
                        logfile = open(file_name2, 'w')
                        logfile.close()
                        file_name = file_name2
                        break
                else:
                    print('Invalid input.')
                    input('Press enter to continue.')
                    continue
        else:
            logfile = open(file_name, 'w')
            logfile.close()
        self.write_logfile = True
        self.log_file = file_name
            


def signal_handler(signal, frame):
	'''
	***********************************************************************
	* Method name:    signal_handler
	* Method purpose: To Catch Interrupt Signal (Ctrl + C) and exit program
	* Date created:   January 14, 2014
	* Last modified:  January 14, 2014, by: Vincian
	* Parameters:     String, Integer
	* Return:         Void
	***********************************************************************
	'''
	print("\n[ Interrupt Received ] Thank you for using me!",end="\n")
	os._exit(1)



def main():
    '''
    ***********************************************************************
    * Method name:    main
    * Method purpose: Main driver method to run the program
    * Date created:   January 19, 2014
    * Last modified:  January 25, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Void
    ***********************************************************************
    '''
    signal.signal(signal.SIGINT, signal_handler)
    scanner=mc_nb_scan()
    starttime=datetime.datetime.now()
    parser = argparse.ArgumentParser()
    if os.name=='nt':
        try:
            data=os.popen('ipconfig /all').read()
            ipconfig_output = io.StringIO(data)
            for line in ipconfig_output:
                if ('IPv4' in line):
                    sub = line.find(':')
                    ip_addr4nt = line[(sub+1):]
                    ip_addr4nt = ip_addr4nt.strip()
                    if ('(Preferred)' in ip_addr4nt):
                        ip_addr4nt = ip_addr4nt.replace('(Preferred)','')
                        ip_addr4nt = ip_addr4nt.strip()
                if ('Subnet Mask' in line):
                    sub = line.find(':')
                    subnet_mask4nt = line[(sub+1):]
                    subnet_mask4nt = subnet_mask4nt.strip()
            cidrPrefix=scanner.ip2bin(subnet_mask4nt).count('1')
            host_range=[ip_addr4nt+'/'+str(cidrPrefix)]
        except:
            print('Could not find IP address and subnet mask for this machine.')
            sys.exit(0)
    elif os.name=='posix':
        data=os.popen('ifconfig | grep \"inet addr\"').read()
        ip=re.findall(r':.*Bcast',data)[0].replace('Bcast','').replace(':','')
        struc=re.findall(r''+ip+'.*Bcast.*Mask.*',data)[0].replace('Bcast:','').replace('Mask:','')
        struc=re.split(' +',struc)
        ip=struc[0]
        mask=struc[2]
        cidrPrefix=scanner.ip2bin(mask).count('1')
        host_range=[ip+"/"+str(cidrPrefix)]
    parser.add_argument('-t', '--type', default='n', nargs=1, help='type of scan to be performed. enter m for MAC address, n for NetBIOS name, mn for both. (both is default.)')
    parser.add_argument('-v','--verbose', nargs="?",const='1', help='Verbose Mode (Display Errors and Messages)')
    parser.add_argument('host_range', nargs="*",default=host_range, help='inclusive range of hosts to be scanned. ex: 192.168.5.1 192,168.5.255')
    parser.add_argument('-w', '--write', nargs=1, help='name of file to write output of scan to. ex: -w logfile.txt (scan output is only printed to console by default.')
    args = parser.parse_args()
    if(type(args.host_range)==str):
        string=args.host_range
        args.host_range=['']
        for i in string:
            args.host_range[0]=args.host_range[0]+i
    print("Scan Started at "+str(starttime)+"..\n")
    try:
        try:
            if int(args.verbose[0])==1:
                scanner.verbose=1
        except:
            pass
        if len(args.host_range)==1:
            try:
                args.host_range[0].index("/")
                scanner.host_range=[args.host_range[0].split('/')[0]]
                if int(args.host_range[0].split('/')[1])>=0 and int(args.host_range[0].split('/')[1])<=32:
                    if scanner.valid_ip():
                        scanner.host_range=args.host_range
                        scanner.generate()
                        continue_scan=1
            except:
                try:
                    args.host_range[0].index(",")
                    for i in range(len(args.host_range[0].split(","))):
                        scanner.host_range.append(args.host_range[0].split(",")[i])
                    continue_scan=scanner.valid_ip()
                except:
                    scanner.host_range=[args.host_range[0]]
                    continue_scan=scanner.valid_ip()
                    pass
        else:
            begin_ip = args.host_range[0]
            end_ip = args.host_range[1]
            first_octets = begin_ip.split('.')[0] + '.' + begin_ip.split('.')[1] + '.' + begin_ip.split('.')[2] + '.'    
            begin_last_octet = int(begin_ip.split('.')[3])
            end_last_octet = int(end_ip.split('.')[3])
            scanner.create_range(begin_last_octet,end_last_octet,first_octets)
            continue_scan = scanner.valid_ip()
        if (continue_scan):
            pass
        else:
            print('Could not validate IP addresses.')
            os._exit(0)
    except:
        print('Could not validate IP addresses.')
        os._exit(0)
    try:
        if (args.type != None):
            scan_type = args.type
            scan_type = scan_type[0]
            if (scan_type == 'mn' or scan_type == 'nm'):
                scan_type='n'
            if (scan_type == 'm' or scan_type == 'n'):
                scanner.scan_type = scan_type
        else:
            scan_type="mn"
            scanner.scan_type = "n"
        if (scanner.scan_type=='m'):
            print("======================================\n    Address\t\t    MAC\n======================================\n")
        elif (scanner.scan_type=='n'):
            print("================================================================\n    Address\t\t    MAC\t\t\t  Name\n================================================================\n")
    except:
        print('Could not resolve scan type.')
        os._exit(0)
    try:
        if (args.write != None):
            logfilename = args.write[0]
            scanner.create_log(logfilename)
    except:
        print('Could not create log file.')
    try:
        Threads=[]
        numthread=20
        if len(scanner.host_range)<15:
            numthread=len(scanner.host_range)
        hostperthread=int(len(scanner.host_range)/numthread)
        addextra=len(scanner.host_range)%numthread
        if (os.name == 'posix'):
            for i in range(numthread):
                arg1=((i+1)*hostperthread)-(hostperthread)
                arg2=arg1+hostperthread
                t = threading.Thread(target=scanner.macresolve4nix, args=(arg1,arg2))
                t.start()
                Threads.append(t)
        elif (os.name == 'nt'):
            for i in range(numthread):
                arg1=((i+1)*hostperthread)-(hostperthread)
                arg2=arg1+hostperthread
                t = threading.Thread(target=scanner.macresolve4nt, args=(arg1,arg2))
                t.start()
                Threads.append(t)
        else:
            print('Could not resolve operating system.')
            sys.exit(0)
    except:
        print('Fatal Error Occurred With MAC and NetBios Name Functions')
        sys.exit(0)
    for thread in Threads:
        thread.join()
    stoptime=datetime.datetime.now()
    print("\n["+str(scanner.counter)+" Scan Attempts Successfull in "+str(stoptime-starttime)+ "]",end="\n")



if (__name__ == '__main__'):
    main()
