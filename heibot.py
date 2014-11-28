import sys;
import socket;
import string;

global heicounter;

HOST = "irc.mibbit.net";
PORT = 6667;
NICK = "heibot";
CHANNEL = "#easyctf";

s = socket.socket();
s.connect((HOST, PORT));
s.send("NICK "+NICK+"\n");
s.send("USER "+NICK+" "+NICK+" "+NICK+" :"+NICK+"\n");

heicounter = 0;

connected = False;
stop = False;
greet = False;
irc = {
    "chan": "#easyctf",
}

def parse(line):
    if line.find("heibot leave") != -1:
        s.send("QUIT\n");
    else:
        if len(line.split(":")) == 3:
            username = line.split(":")[1].split("!")[0];
            message = line.split(":")[2];
            if message.strip() in ["hi", "hei", "hello"]:
                s.send("PRIVMSG %s :hei, %s\n" % (irc['chan'], username));
            if message.find("!") != -1:
                actual = message[1:];
                command = actual.split(" ")[0];
                if command.find("count") != -1:
                    print "nothing is done";

while not stop:
    line = s.recv(1024);
    print line;
    if line.find("PRIVMSG %s" % irc['chan']) != 1:
        parse(line);
    if line.find("PING") != -1:
        s.send("PONG :" + line.split(":")[1]);
        if not connected:
            s.send("JOIN %(chan)s\n" % irc);
            if not greet:
                greet = True;
                s.send("PRIVMSG %(chan)s :hei\n" % irc);
    if stop:
        break;

