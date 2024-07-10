from datetime import datetime
import json
import re
import shutil

class MessageType:
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    STICKER = "STICKER"
    CALL = "CALL"
    VIDEOCALL = "VIDEOCALL"

class Message:
    # It is important to keep the order of the functions
    # as each function will trim the line to make it easier to parse
    def __init__(self, line):
        self.__line = line
        self.date = self._parse_date_()
        self.sender = self._parse_sender_()
        self.message = self._parse_message_()
        self.type = self.__type()
    
    def __str__(self):
        return f"{self.date} - {self.sender}: {self.message}"
    
    def __type(self):
        if "Llamada" in self.message and ("min" in self.message or "h" in self.message):
            return MessageType.CALL
        elif "Videollamada" in self.message and ("min" in self.message or "h" in self.message):
            return MessageType.VIDEOCALL
        elif "sticker omitido" in self.message:
            return MessageType.STICKER
        elif "imagen omitida" in self.message:
            return MessageType.IMAGE
        elif "Video omitido" in self.message:
            return MessageType.VIDEO
        else:
            return MessageType.TEXT

    def _parse_date_(self):
        date_str = ""
        i = 1
        while i < len(self.__line):
            char = self.__line[i]
            if char == ']':
                break
            else:
                date_str += char
            i += 1
        corrected_date_str = date_str.replace('a.m.', 'AM').replace('p.m.', 'PM')
        self.__line = self.__line[i + 2:]
        try:
            dateTime = datetime.strptime(corrected_date_str, "%m/%d/%y, %I:%M:%S %p")
            return dateTime
        except ValueError as e:
            print(f"Error parsing date: {date_str} - {e}")
            return None
        
    def _parse_sender_(self): 
        sender_str = ""
        i = 0
        while i < len(self.__line):
            if self.__line[i] == ':':
                self.__line = self.__line[i+2:]
                break
            sender_str += self.__line[i]
            i+=1
        return sender_str
    
    def _parse_message_(self):
        return self.__line
    
    def get_sender(self):
        return self.sender

    def get_date(self) -> datetime:
        return self.date
    
    def get_message(self):
        return self.message
    
    def get_epoch(self) -> float:
        return self.date.timestamp()
    
    def get_message_length(self):
        return len(self.message)
    
    def get_duration(self):
        if self.type == MessageType.CALL or self.type == MessageType.VIDEOCALL:
            num = self.message.split()[-2]
            metric = self.message.split()[-1]
            if metric == "min":
                return int(num)
            elif metric == "h":
                return int(num) * 60
        return None
            

class Chatty:
    def __init__(self, file):
        self.file = file
        self.messages: list[Message] = []

    def _is_start_of_message_(self, line):
        if not line or len(line) < 2:
            return False
        if line[0] == '[':
            return True
        # elif line[1] == '[':
        #     return True
        return False    

    def open_file(self):
        f = open(self.file, "r")
        line = f.readline()
        while line:
            line = f.readline()
            line = line.replace('\u200e', ' ').replace('\u202f', ' ')
            if self._is_start_of_message_(line):
                self.messages.append(Message(line))
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
    
    def get_senders(self):
        return set([message.get_sender() for message in self.messages])
    
    def get_message_by_message(self, message):
        return [m for m in self.messages if m.get_message() == message]
    
    def get_images(self):
        return [m for m in self.messages if m.type == MessageType.IMAGE]
    
    def get_videocalls(self):
        return [m for m in self.messages if m.type == MessageType.VIDEOCALL]

    def get_calls(self):
        return [m for m in self.messages if m.type == MessageType.CALL]
    
    def get_stickers(self):
        return [m for m in self.messages if m.type == MessageType.STICKER]
    
    def get_videos(self):
        return [m for m in self.messages if m.type == MessageType.VIDEO]
    
    def get_total_messages(self):
        return len(self.messages)
    
    def get_longest_message(self):
        return max(self.messages, key=lambda x: x.get_message_length())
    
    def get_shortest_message(self):
        return min(self.messages, key=lambda x: x.get_message_length())
    
    def get_average_message_length(self):
        return sum([m.get_message_length() for m in self.messages]) / len(self.messages)
    
    def get_total_messages_by_sender(self, sender):
        return len(self.get_messages_by_sender(sender))
    
    def get_total_minutes_in_calls(self):
        return sum([m.get_duration() for m in self.get_calls()])
    
    def get_total_minutes_in_videocalls(self):
        return sum([m.get_duration() for m in self.get_videocalls()])
    
    def get_message_that_contains(self, text):
        return [m for m in self.messages if text in m.get_message()]
    
    def get_total_messages_by_day(self):
        days = {}
        for message in self.messages:
            day = f"{message.get_date().day}/{message.get_date().month}/{message.get_date().year}"
            if day in days:
                days[day] += 1
            else:
                days[day] = 1
        sorted_days = {k: v for k, v in sorted(days.items(), key=lambda item: item[1], reverse=True)}

        return sorted_days
    
    def get_total_messages_by_month(self):
        months = {}
        for message in self.messages:
            month = f"{message.get_date().month}/{message.get_date().year}"
            if month in months:
                months[month] += 1
            else:
                months[month] = 1
        sorted_months = {k: v for k, v in sorted(months.items(), key=lambda item: item[1], reverse=True)}

        return sorted_months
            


if __name__ == "__main__": 
    c = Chatty("_chat.txt")
    c.open_file()
    print(c.get_longest_message())
    print(f"Total images: {len(c.get_images())}")
    print("Total stickers: ", len(c.get_stickers()))
    print("Total videos: ", len(c.get_videos()))
    print(f"Total mins in calls: {c.get_total_minutes_in_calls()}")
    print(f"Total mins in videocalls: {c.get_total_minutes_in_videocalls()}")
    print(f"Total mins in videocalls + calls: {c.get_total_minutes_in_videocalls() + c.get_total_minutes_in_calls()}")
    print(json.dumps(c.get_total_messages_by_month(), indent=4))