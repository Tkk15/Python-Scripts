'''
Python Security Toolkit
IRC Bot
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
import io
import os.path



class irc_bot():
    '''
    ***********************************************************************
    * Class Name: 	irc_bot
    * Class Purpose:	To hold methods and data associated with an
    *     instance of the irc_bot class
    * Date created: 	January 13, 2014
    * Last modified: 	January 13, 2014, by: bbishop423
    ***********************************************************************
    '''
    server = ''
    channel = ''
    botnick = ''
    realname = ''
    owner_list = []
    botsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    help_file = '''start bot command help!!!
                          
just private msg the bot followed with the command and parameter(s)
                          
example:
                          
/msg botsnick $op mynick
(where botsnick is the nickname you have designated of the bot, and mynick is the nick of the person you want to op)
**** bot sets mynick to op ****
                          
                          
parameters are designated with < >
(this means substitute the name of the channel or nick, etc... at these places, leave out the < > when you type yours in!)
                          
                          
----Command list with parameters----    ----Description of what the commands make the bot do ----
                          
$op <channel> <nick>                    ---gives ops to specified user in specified channel
$deop <channel> <nick>                  ---removes ops for specified user in specified channel
$kick <channel> <nick>                  ---kicks specified user in specified channel
$inv <channel> <nick>                   ---invites specified user to specified channel
$nick <new nick>                        ---changes nick of bot
$join <channel>                         ---joins channel
$leave <channel>                        ---leaves channel
$quit                                   ---disconnects from server
$setname <real name>                    ---sets real name of bot
$topic <channel> <new topic>            ---sets topic for specified channel
$privmsg <nick> <message>               ---private msgs user
$msg <channel> <message>                ---sends message to specified channel
$voice <channel> <nick>                 ---gives voice to a user of specified channel
$half <channel> <nick>                  ---gives halfops to a user of specified channel
$admin <channel> <nick>                 ---gives admin to a user of specified channel
$owner <channel> <nick>                 ---gives owner status of specified channel to a user
$ban <channel> <nick!ident@host>        ---bans a user <nick!ident@host> from specified channel
$unban <channel> <nick!ident@host>      ---unbans a user <nick!ident@host> from specified channel
$adduser <nick>                         ---adds nick to the list of authorized users
$rmuser <nick>                          ---removes nick from the list of authorized users
$users                                  ---sends list of authorized users to user in private message
$help                                   ---sends bot instructions to user in private message
                          
end bot command help!!!
'''

    def __init__(self,serv,chan,botnk,realnm,ownr):
        '''
        ***********************************************************************
        * Method name:    __init__
        * Method purpose: To create an instance of the irc_bot class
        * Date created:   January 13, 2014
        * Last modified:  January 13, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Void
        ***********************************************************************
        '''
        self.server = serv
        self.channel = chan
        self.botnick = botnk
        self.realname = realnm
        self.owner_list.append(ownr)



    def getowners(self,usr):
        '''
        ***********************************************************************
        * Method name:    getowners
        * Method purpose: To retrieve the list of authorized users of this bot
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     None
        * Return:         List of Strings
        ***********************************************************************
        '''
        for name in self.owner_list:
            self.sendprivmsg(usr,name)
            time.sleep(1)



    def addusr(self,user_to_add,usr_to_answer):
        '''
        ***********************************************************************
        * Method name:    addusr
        * Method purpose: To add a nick to the list of authorized users
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String, String
        * Return:         Void
        ***********************************************************************
        '''
        try:
            self.owner_list.append(user_to_add)
            self.sendprivmsg(usr_to_answer,user_to_add + "was added to list of authorized users.")
        except:
            self.sendprivmsg(usr_to_answer,"could not add " + user_to_add + " to list of authorized users.")



    def remusr(self,user_to_remove,usr_to_respond):
        '''
        ***********************************************************************
        * Method name:    remusr
        * Method purpose: To remove a nick from the list of authorized users
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String, String
        * Return:         Void
        ***********************************************************************
        '''
        try:
            if (len(self.owner_list) > 1):
                self.owner_list.remove(user_to_remove)
                self.sendprivmsg(usr_to_respond,user_to_remove + "was removed from the list of authorized users.")
            else:
                self.sendprivmsg(usr_to_respond,"can't remove only remaining authorized user.")
        except:
            self.sendprivmsg(usr_to_respond,"could not remove " + user_to_remove + " from list of authorized users.")



    def bothelp(self,usr):
        '''
        ***********************************************************************
        * Method name:    bothelp
        * Method purpose: To display the bot help file to an authorized user
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String
        * Return:         Void
        ***********************************************************************
        '''
        try:
            output = io.StringIO(self.help_file)
            for line in output:
                self.sendprivmsg(usr,line)
                time.sleep(1)
            output.close()
        except:
            self.sendprivmsg(usr,"error! could not load instructions!")



    def ping(self):
        '''
        ***********************************************************************
        * Method name:    ping
        * Method purpose: To respond to server pings
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Void
        ***********************************************************************
        '''
        self.botsock.send(str.encode("PONG :pingis\n"))



    def sendmsg(self,chanToMsg,msg_for_chan):
        '''
        ***********************************************************************
        * Method name:    sendmsg
        * Method purpose: To send a message to a specified channel
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String, String
        * Return:         Void
        ***********************************************************************
        '''
        self.botsock.send(str.encode("PRIVMSG " + chanToMsg + " :" + msg_for_chan + "\n"))



    def sendprivmsg(self,user_nick,private_msg):
        '''
        ***********************************************************************
        * Method name:    sendprivmsg
        * Method purpose: To send a private message to a specified user
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String, String
        * Return:         Void
        ***********************************************************************
        '''
        self.botsock.send(str.encode("PRIVMSG " + user_nick + " :" + private_msg + "\n"))



    def joinchan(self,chan):
        '''
        ***********************************************************************
        * Method name:    joinchan
        * Method purpose: To join a specified channel
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String
        * Return:         Void
        ***********************************************************************
        '''
        self.botsock.send(str.encode("JOIN " + chan + "\n"))



    def hello(self):
        '''
        ***********************************************************************
        * Method name:    hello
        * Method purpose: To respond when someone says Hello <bot's nick>
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Void
        ***********************************************************************
        '''
        self.botsock.send(str.encode("PRIVMSG " + self.channel + " :Hello!\n"))



    def writelog(self,msg,log_name):
        '''
        ***********************************************************************
        * Method name:    writelog
        * Method purpose: To write a log of the chat to a file
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String
        * Return:         Void
        ***********************************************************************
        '''
        try:
            log_file = open(log_name,'a')
            log_file.write(msg + '\n')
            log_file.close()
        except:
            print('error! could not write to log file!')



    def parsemsg(self,msg,btnk):
        '''
        ***********************************************************************
        * Method name:    parsemsg
        * Method purpose: To parse messages sent to the bot to see if they
        *     are commands sent by authorized users
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     String, String
        * Return:         Void
        ***********************************************************************
        '''
        msg = msg.split(":")
        cmd = msg[2]
        cmd = cmd.split(" ")
        is_cmd = cmd[0]
        find_who = msg[1].split("!")
        who = find_who[0]
        find_to_who = msg[1].split(" ")
        for name in self.owner_list:
            if (who == name):
                if (find_to_who[2] == self.botnick):
                    if (is_cmd[0] == "$"):
                        try:
                            if (cmd[0] == "$op"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +o " + cmd[1] + "\n"))
                            elif (cmd[0] == "$deop"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " -o " + cmd[1] + "\n"))
                            elif (cmd[0] == "$kick"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("KICK " + cmd[0] + " " + cmd[1] + " Bye Bye Bye!\n"))
                            elif (cmd[0] == "$inv"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("INVITE " + cmd[1] + " " + cmd[0] + "\n"))
                            elif (cmd[0] == "$nick"):
                                self.botsock.send(str.encode("NICK " + cmd[1] + "\n"))
                            elif (cmd[0] == "$join"):
                                self.botsock.send(str.encode("JOIN " + cmd[1] + "\n"))
                            elif (cmd[0] == "$leave"):
                                self.botsock.send(str.encode("PART " + cmd[1] + "\n"))
                            elif (cmd[0] == "$quit"):
                                self.botsock.send(str.encode("QUIT :Bye Bye Bye!\n"))
                            elif (cmd[0] == "$setname"):
                                self.botsock.send(str.encode("SETNAME " + cmd[1] + "\n"))
                            elif(cmd[0] == "$topic"):
                                cmd.pop(0)
                                topic_chan = cmd.pop(0)
                                topic = " ".join(cmd)
                                self.botsock.send(str.encode("TOPIC " + topic_chan + " :" + topic + "\n"))
                            elif (cmd[0] == "$privmsg"):
                                cmd.pop(0)
                                msg_to = cmd.pop(0)
                                msg_to_send = " ".join(cmd)
                                self.sendprivmsg(msg_to,msg_to_send)
                            elif (cmd[0] == "$msg"):
                                cmd.pop(0)
                                channel_to_msg = cmd.pop(0)
                                msgToSend = " ".join(cmd)
                                self.sendmsg(channel_to_msg,msgToSend)
                            elif (cmd[0] == "$voice"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +v " + cmd[1] + "\n"))
                            elif (cmd[0] == "$half"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +h " + cmd[1] + "\n"))
                            elif (cmd[0] == "$admin"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +a " + cmd[1] + "\n"))
                            elif (cmd[0] == "$owner"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +q " + cmd[1] + "\n"))
                            elif (cmd[0] == "$ban"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +b " + cmd[1] + "\n"))
                            elif (cmd[0] == "$unban"):
                                cmd.pop(0)
                                self.botsock.send(str.encode("MODE " + cmd[0] + " +e " + cmd[1] + "\n"))
                            elif (cmd[0] == "$users"):
                                self.getowners(who)
                            elif (cmd[0] == "$adduser"):
                                cmd.pop(0)
                                usr_to_add = cmd[0]
                                self.addusr(usr_to_add,who)
                            elif (cmd[0] == "$rmuser"):
                                cmd.pop(0)
                                usr_to_rm = cmd[0]
                                self.remusr(usr_to_rm,who)
                            elif (cmd[0] == "$help"):
                                self.bothelp(who)
                            else:
                                self.sendprivmsg(who,"not a valid command! enter $help for a list of instructions.")
                        except:
                            self.sendprivmsg(who,"error! could not execute command! enter $help for a list of instructions.")
                    else:
                        self.sendprivmsg(who,"error! could not execute command! enter $help for a list of instructions.")



    def connect(self):
        '''
        ***********************************************************************
        * Method name:    connect
        * Method purpose: To connect the bot to a server
        * Date created:   January 13, 2014
        * Last modified:  January 14, 2014, by: bbishop423
        * Parameters:     None
        * Return:         Boolean
        ***********************************************************************
        '''
        try_connect = False
        try:
            self.botsock.connect((self.server, 6667))
            self.botsock.send(str.encode("USER " + self.botnick + " " + self.botnick + " " + self.botnick + " :PyST\n"))
            self.botsock.send(str.encode("NICK " + self.botnick + "\n"))
            self.botsock.send(str.encode("SETNAME " + self.realname + "\n"))
            self.joinchan(self.channel)
            try_connect = True
        except:
            print('error! could not connect ' + self.botnick + ' to ' + self.server)
        return try_connect



def write_file():
    '''
    ***********************************************************************
    * Method name:    write_file
    * Method purpose: Method to check and create output file
    * Date created:   January 14, 2014
    * Last modified:  January 14, 2014, by: bbishop423
    * Parameters:     None
    * Return:         String
    ***********************************************************************
    '''
    logfile_name = input("Enter name for log file: ")
    while True:
        file_exist = os.path.isfile(logfile_name)
        if (file_exist == True):
            overwrite_file = input("File already exists. Do you wish to overwrite it? (y/n): ")
            overwrite_file = overwrite_file.lower()
            overwrite_file = overwrite_file[0]
            if (overwrite_file == "y"):
                logfile = open(logfile_name,'w')
                logfile.close()
                break
            elif (overwrite_file == "n"):
                logfile_name = input("Enter name for log file: ")
                continue
            else:
                print('Invalid input.')
                input('Press enter to continue.')
                print('\n'*75)
                continue
        else:
            logfile = open(logfile_name,'w')
            logfile.close()
            break
    return logfile_name



def main():
    '''
    ***********************************************************************
    * Method name:    main
    * Method purpose: Main driver method to run the program
    * Date created:   January 13, 2014
    * Last modified:  January 14, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Void
    ***********************************************************************
    '''
    print('\n'*75)
    print("Python Security Toolkit")
    print("IRC Bot")
    print("--------------------------\n")
    usr_server = input('Enter server to connect to: ')
    usr_channel = input('Enter channel to join: ')
    usr_botnick = input("Enter bot's nick: ")
    usr_realnm = input("Enter real name for bot: ")
    usr_owner = input("Enter your IRC nick to add to list of authorized users: ")
    while True:
        write_log = input("Do you wish to save the IRC log to a file? (y/n): ")
        if (len(write_log) > 0):
            write_log = write_log.lower()
            write_log = write_log[0]
            if (write_log == "y"):
                want_log = True
                logfile_name = write_file()
                break
            elif (write_log == "n"):
                print("IRC log will be printed to console only.")
                want_log = False
                break
            else:
                print("Invalid input.")
                input("Press enter to continue.")
                print('\n'*75)
                continue
        else:
            print("Invalid input.")
            input("Press enter to continue.")
            print("\n"*75)
            continue
    bot = irc_bot(usr_server,usr_channel,usr_botnick,usr_realnm,usr_owner)
    connection_valid = bot.connect()
    if (connection_valid):
        while True:
            ircmsg = bot.botsock.recv(2048)
            ircmsg = bytes.decode(ircmsg)
            ircmsg = ircmsg.strip('\n\r')
            print(ircmsg)
            if (ircmsg.find("PING :") != -1):
                bot.ping()
            if (ircmsg.find(":Hello " + bot.botnick) != -1):
                bot.hello()
            if (ircmsg.find("PRIVMSG") != -1):
                bot.parsemsg(ircmsg,bot.botnick)
                if (want_log == True):
                    bot.writelog(ircmsg,logfile_name)



if (__name__ == '__main__'):
    main()
