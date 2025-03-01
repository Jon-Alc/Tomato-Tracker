class LogEntry():

    def __init__(self, message_id, message_url, message_date, log_duration, log_streak):
        self.id = message_id
        self.url = message_url
        self.date = message_date
        self.time = log_duration
        self.streak = log_streak

    def __str__(self):
        return f"\
              id: {self.id}\n\
              url: {self.url}\n\
              date: {self.date}\n\
              time: {self.time}\n\
              streak: {self.streak}\n\
              "