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

while 1:
    line = s.recv(1024);
    print line;
    if line.find("PING") != -1:
        s.send("PONG :" + line.split(":")[1]);
        s.send("JOIN #easyctf\n");

