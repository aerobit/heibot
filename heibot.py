import sys;
import socket;
import string;

HOST = "irc.mibbit.net";
PORT = 6667;
NICK = "heibot";
CHANNEL = "#easyctf";

s = socket.socket();
s.connect((HOST, PORT));
s.send("NICK "+NICK+"\n");
s.send("USER "+NICK+" "+NICK+" "+NICK+" :"+NICK+"\n");

connected = False;
stop = False;
irc = {
    "chan": "#easyctf",
}

def parse(line):
    if line.find("heibot leave") != -1:
        s.send("QUIT\n");
        stop = True;

while not stop:
    line = s.recv(1024);
    print line;
    if line.find("PRIVMSG") != 1:
        parse(line);
    if line.find("PING") != -1:
        s.send("PONG :" + line.split(":")[1]);
        if not connected:
            s.send("JOIN %(chan)s\n" % irc);
            s.send("PRIVMSG %(chan)s hei\n" % irc);
    if stop:
        break;

