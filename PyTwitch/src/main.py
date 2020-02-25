import socket
import pyautogui
import threading

CONFIG = dict(SERVER = 'irc.twitch.tv', PORT = 6667, PASSWORD = 'oauth:zb7rszwipezbov3bocq3prttduap4z', BOTNAME = 'TwitchPlay', CHANNEL = 'kotesky', OWNER = 'kotesky')
irc = socket.socket()
irc.connect((CONFIG['SERVER'], CONFIG['PORT']))
irc.send(("PASS " + CONFIG['PASSWORD'] + "\n" +
          "NICK " + CONFIG['BOTNAME'] + "\n" +
          "JOIN #" + CONFIG['CHANNEL'] + "\n").encode())
message = ''


def game_controller():
    global message
    while True:
        if "up" in message.lower():
            pyautogui.keyDown('w')
            message = ''
            pyautogui.keyUp('w')
        elif "down" in message.lower():
            pyautogui.keyDown('s')
            message = ''
            pyautogui.keyUp('s')
        elif "right" in message.lower():
            pyautogui.keyDown('d')
            message = ''
            pyautogui.keyUp('d')
        elif "left" in message.lower():
            pyautogui.keyDown('a')
            message = ''
            pyautogui.keyUp('a')
        elif "act" in message.lower():
            pyautogui.keyDown('f')
            message = ''
            pyautogui.keyUp('f')
        elif "menu" in message.lower():
            pyautogui.keyDown('esc')
            message = ''
            pyautogui.keyUp('esc')
        elif "map" in message.lower():
            pyautogui.keyDown('m')
            message = ''
            pyautogui.keyUp('m')
        elif "rmenu" in message.lower():
            pyautogui.keyDown('right')
            message = ''
            pyautogui.keyUp('right')
        elif "lmenu" in message.lower():
            pyautogui.keyDown('left')
            message = ''
            pyautogui.keyUp('left')
        else: pass

def twich_controller():
    global message
    def join_chat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = loading_completed(line)

    def loading_completed(line: str)-> bool :
        if("End of /NAMES list" in line):
            print('Bot entrou no canal' + CONFIG['CHANNEL'])
            send_message(irc, "Entrou no canal")
            return False
        else: return True

    def send_message(irc, message:str):
        messageTemp = "PRIVMSG #" + CONFIG['CHANNEL'] + " :" + message
        irc.send((messageTemp + "\n").encode())

    def get_user(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def get_message(line): 
        try: message = (line.split(":",2)[2])
        except: message = ""
        return message

    def console(line):
        if "PRIVMSG" in line:
            return True
        else: return False
        
    join_chat()

    while True: 
        try:
            readbuffer = irc.recv(1024).decode()
        except: readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and console(line):
                msg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msg)
                print(msg)
                continue
            else:
                print(line)
                user = get_user(line)
                message = get_message(line)
                print(user + " : " + message)
                
if __name__ == '__main__':
    twThread = threading.Thread(target=twich_controller)
    twThread.start()
    gameThread = threading.Thread(target=game_controller)
    gameThread.start()