from datetime import datetime

class Message:
    # It is important to keep the order of the functions
    # as each function will trim the line to make it easier to parse
    def __init__(self, line):
        self.line = line
        self.date = self._parse_date_()
        self.sender = self._parse_sender_()
        self.message = self._parse_message_()
    
    def __str__(self):
        return f"{self.date} - {self.sender}: {self.message}"

    def _parse_date_(self):
        date_str = ""
        i = 1
        while i < len(self.line):
            char = self.line[i]
            if char == ']':
                break
            if char == '\u202f':
                date_str += " "
            else:
                date_str += char
            i += 1
        corrected_date_str = date_str.replace('a.m.', 'AM').replace('p.m.', 'PM')
        self.line = self.line[i + 2:]
        try:
            dateTime = datetime.strptime(corrected_date_str, "%m/%d/%y, %I:%M:%S %p")
            return dateTime
        except ValueError as e:
            print(f"Error parsing date: {date_str} - {e}")
            return None
        
    def _parse_sender_(self): 
        sender_str = ""
        i = 0
        while i < len(self.line):
            if self.line[i] == ':':
                self.line = self.line[i+2:]
                break
            sender_str += self.line[i]
            i+=1
        return sender_str
    
    def _parse_message_(self):
        return self.line
    
    def get_sender(self):
        return self.sender

    def get_date(self) -> datetime:
        return self.date
    
    def get_message(self):
        return self.message
    
    def get_epoch(self) -> float:
        return self.date.timestamp()
    
    def get_message_length(self):
        return len(self.message.split())

class Chatty:
    def __init__(self, file):
        self.file = file
        self.messages = []

    def _is_start_of_message_(self, line):
        if not line or len(line) < 2:
            return False
        if line[0] == '[':
            return True
        return False    

    def open_file(self):
        f = open(self.file, "r")
        line = f.readline()
        c = 0
        while line:
            line = f.readline()
            c += 1
            if self._is_start_of_message_(line):
                self.messages.append(Message(line))
        print(f"Total lines read: {c}")
        f.close()

    def get_messages(self):
        return self.messages
    
    def get_messages_by_sender(self, sender):
        return [message for message in self.messages if message.get_sender() == sender]
    
    def get_messages_by_date(self, date):
        start = datetime(date.year, date.month, date.day, 0, 0, 0).timestamp()
        end = datetime(date.year, date.month, date.day, 23, 59, 59).timestamp()
        return self.get_messages_between_epochs(start, end)
    
    def get_messages_by_epoch(self, epoch):
        return [message for message in self.messages if message.get_epoch() == epoch]
    
    def get_messages_between_epochs(self, start, end):
        return [message for message in self.messages if message.get_epoch() >= start and message.get_epoch() <= end]
    
    def get_longest_message(self):
        return max(self.messages, key=lambda x: x.get_message_length())
    
    def get_shortest_message(self):
        return min(self.messages, key=lambda x: x.get_message_length())
    
    def get_average_message_length(self):
        return sum([m.get_message_length() for m in self.messages]) / len(self.messages)
    
    def get_total_messages(self):
        return len(self.messages)
    
    def get_total_messages_by_sender(self, sender):
        return len(self.get_messages_by_sender(sender))
    
    def get_senders(self):
        return set([message.get_sender() for message in self.messages])
    
    def get_message_by_message(self, message):
        return [m for m in self.messages if m.get_message() == message]

if __name__ == "__main__": 
    c = Chatty("_chat.txt")
    c.open_file()
    m = c.get_messages_by_date(datetime(2024, 7, 2))
    for message in m:
        print(message)

    
