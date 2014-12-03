import sys;
import socket;
import string;
import random;

HOST = "irc.mibbit.net";
PORT = 6667;
NICK = "heibot";
CHANNEL = "#easyctf";

words = [i for i in open("wordlist.txt").read().split("\n") if len(i)>4];
outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again ", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "no.", "START", "A", "B", "UP", "DOWN", "LEFT", "RIGHT", "SELECT"];

s = socket.socket();
s.connect((HOST, PORT));
s.send("NICK "+NICK+"\n");
s.send("USER "+NICK+" "+NICK+" "+NICK+" :"+NICK+"\n");

heicounter = 0;

connected = False;
stop = False;
greet = False;
irc = {
    "chan": CHANNEL,
}

# f = open("log.txt", "a");

bitches = set();
commands = ["help", "helixfossil (or hf)", "md5", "roll", "flag", "rek", "<3", "top", "solved"];

def generate_flag():
    flag = "";
    for i in range(6):
        if i != 0:
            flag += "_";
        flag += random.choice(words);
    return flag;

def parse(line):
    if False: #line.find("heibot leave") != -1:
        # f.close();
        s.send("QUIT\n");
        s.send("NICK "+NICK+"\n");
        s.send("USER "+NICK+" "+NICK+" "+NICK+" :"+NICK+"\n");
    else:
        if line.find("JOIN :#easyctf") != -1:
            username = line.split(":")[1].split("!")[0];
            # s.send("PRIVMSG %s :welcome, %s\n" % (irc['chan'], username));
            if username.lower().find("bot") != -1:
                string = "KICK %s %s :heibot is the only real bot\n" % (irc['chan'], username);
                print string;
                s.send(string);
        if len(line.split(":")) == 3:
            username = line.split(":")[1].split("!")[0];
            message = line.split(":")[2];
            if message.split(" ")[0].strip().strip(",").strip(":").lower() in ["hi", "hei", "hello"]:
                random.seed();
                k = random.randint(1, 1000);
                if k < 900:
                    s.send("PRIVMSG %s :hei, %s\n" % (irc['chan'], username));
                else:
                    s.send("PRIVMSG %s :fuck you, %s, i hope you die a horribly gruesome death\n" % (irc['chan'], username));
            if message.split(" ")[0].strip().strip(",").strip(":").lower() in ["lol"]:
                s.send("PRIVMSG %s :%s, but did you actually laugh out loud?\n" % (irc['chan'], username));
            if message.find("`") != -1:
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
                elif command.find("help") != -1:
                    s.send("PRIVMSG %s :commands are: %s\n" % (irc['chan'], ", ".join(sorted(commands))));
                elif command.find("flag") != -1:
                    try:
                        problem = message.strip("\r\n")[6:];
                        print problem;
                        if len(problem) < 1:
                            raise Exception();
                        string = "PRIVMSG %s :%s, sending the flag for %s to you in private message!\n" % (irc['chan'], username, problem);
                        print string;
                        s.send(string);
                        s.send("PRIVMSG %s :%s\n" % (username, generate_flag()));
                    except Exception:
                        s.send("PRIVMSG %s :Usage: `flag [problem_name]\n" % (irc['chan']));
                elif command.find("rek") != -1:
                    user = message.strip("\r\n")[5:];
                    print user;
                    try:
                        if len(user) < 1:
                            raise Exception();
                        s.send("PRIVMSG %s :%s, you just got rekt by %s\n" % (irc['chan'], user, username));
                    except Exception:
                        s.send("PRIVMSG %s :Usage: `rek [username]\n" % (irc['chan']));
                elif command.find("md5") != -1:
                    try:
                        stuff = message.strip("\r\n")[5:];
                        print stuff;
                        if len(stuff) < 1:
                            raise Exception();
                        s.send("PRIVMSG %s :md5 of \"%s\" is %s\n" % (irc['chan'], stuff, __import__("hashlib").md5(stuff).hexdigest()));
                    except Exception:
                        s.send("PRIVMSG %s :Usage: `md5 [stuff]\n" % (irc['chan']));
                elif command.find("helixfossil") != -1 or command.find("hf") != -1:
                    s.send("PRIVMSG %s :%s, %s\n" % (irc['chan'], username, random.choice(outcomes)));
                elif command.find("<3") != -1:
                    bitches.add(username);
                    s.send("PRIVMSG %s :<3 %s\n" % (irc['chan'], username));
                elif command.find("bitches") != -1:
                    s.send("PRIVMSG %s :My bitches are: %s\n" % (irc['chan'], ", ".join(list(bitches))));
                elif command.find("top") != -1:
                    num = 5;
                    try:
                        if len(actual) == 2:
                            num = int(actual[1]);
                            if num < 1:
                                raise Exception()
                    except Exception:
                        num = 5;
                        # s.send("PRIVMSG %s :Usage: `top [n]\n" % (irc['chan']));
                    try:
                        data = __import__("json").loads(__import__("urllib2").urlopen("http://easyctf.com/api/stats/top?num=%d" % num).read());
                        string = "";
                        for item in data:
                            string += "%d: %s, %dpts; " % (item['place'], item['teamname'], item['points']);
                        s.send("PRIVMSG %s :top %d teams: %s\n" % (irc['chan'], num, str(string)));
                    except Exception:
                        s.send("PRIVMSG %s :dang it, screwed up somewhere\n" % (irc['chan']));
                elif command.find("solved") != -1:
                    try:
                        stuff = message.strip("\r\n")[8:];
                        print stuff;
                        if len(stuff) < 1:
                            raise Exception();
                        try:
                            data = __import__("json").loads(__import__("urllib2").urlopen("http://easyctf.com/api/stats/solved?pname=%s" % __import__("urllib").pathname2url(stuff)).read());
                            print data;
                            string = "";
                            if data['status'] == 1:
                                string = "%d teams have solved %s!" % (data['nTeams'], stuff);
                            else:
                                string = "error: %s" % (data['message']);
                            s.send("PRIVMSG %s :%s\n" % (irc['chan'], str(string)));
                            if stuff.lower() in ['the door', 'guessing is hard']:
                                s.send("PRIVMSG %s :chaosagent cannot solve %s and therefore deserves public shaming" % (irc['chan'], stuff))
                        except Exception:
                            s.send("PRIVMSG %s :dang it, screwed up somewhere\n" % (irc['chan']));
                    except Exception:
                        s.send("PRIVMSG %s :Usage: `solved [problem_name]\n" % (irc['chan']));

while not stop:
    line = s.recv(1024);
    print line.strip();
    f = open("log.txt", "a");
    f.write("%s\n" % line.strip());
    f.close();
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



