import sys;
import socket;
import string;
import random;

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

f = open("log.txt", "a");

def parse(line):
    if False: # line.find("heibot leave") != -1:
        f.close();
        s.send("QUIT\n");
    else:
        if len(line.split(":")) == 3:
            username = line.split(":")[1].split("!")[0];
            message = line.split(":")[2];
            if message.strip() in ["hi", "hei", "hello"]:
                s.send("PRIVMSG %s :hei, %s\n" % (irc['chan'], username));
            if message.find("!") != -1:
                actual = message[1:].split(" ");
                command = actual[0];
                if command.find("roll") != -1:
                    highest = 1000;
                    try:
                        if len(actual) == 2:
                            highest = int(actual[1]);
                            if highest < 1:
                                raise Exception()
                        s.send("PRIVMSG %s :%s rolled %d\n" % (irc['chan'], username, random.randint(1, highest)));
                    except Exception:
                        a = 0;
                        s.send("PRIVMSG %s :fuck you %s\n" % (irc['chan'], username));

while not stop:
    line = s.recv(1024);
    print line.strip();
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



