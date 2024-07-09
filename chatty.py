from datetime import datetime

class Message:
    # It is important to keep the order of the functions
    # as each function will trim the line to make it easier to parse
    def __init__(self, line):
        self.line = line
        self.date = self._parseDate_()
        self.sender = self._parseSender_()
        self.message = self._parseMessage_()
    
    def _parseDate_(self):
        date = ""
        for i in range(1, len(self.line)):
            if self.line[i] == 'a' or self.line[i] == 'p':
                self.line = self.line[i+6:]
                break
            if self.line[i] == '\u202f':
                date += " "
                continue
            date += self.line[i]
        try:
            dateTime = datetime.strptime(date, "%m/%d/%y, %I:%M:%S ")
            return dateTime
        except:
            return None
        
    def _parseSender_(self): 
        sender = ""
        i = 0
        while i < len(self.line):
            if self.line[i] == ':':
                self.line = self.line[i+2:]
                break
            sender += self.line[i]
            i+=1
        return sender
    
    def _parseMessage_(self):
        message = ""
        i = 0
        while i < len(self.line):
            message += self.line[i]
            i+=1
        return message
    
    def getSender(self):
        return self.sender

    def getDate(self):
        return self.date
    
    def getMessage(self):
        return self.message


def isStartOfMessage(line):
    if not line:
        return False
    if line[0] == '[':
        return True
    return False

def main():
    f = open("_chat.txt", "r")
    line = f.readline()
    messages = {}
    senders = ()
    while line:
        line = f.readline()
        if isStartOfMessage(line):
            m = Message(line)
            if m.getSender() not in messages:
                messages[m.getSender()] = []
            messages[m.getSender()].append(m)
    
    for m in messages:
        print(m, len(messages[m]))

    f.close()

if __name__ == "__main__":
    main()