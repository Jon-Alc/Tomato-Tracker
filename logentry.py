class LogEntry():

    def __init__(self, message_id, message_session, message_url, message_date, log_duration, log_streak):
        self.id = message_id
        self.session = message_session
        self.url = message_url
        self.date = message_date
        self.duration = log_duration
        self.streak = log_streak

    def __str__(self):
        return f"\
              id: {self.id}\n\
              session: {self.session}\n\
              url: {self.url}\n\
              date: {self.date}\n\
              duration: {self.time}\n\
              streak: {self.streak}\n\
              "
    
    def to_list(self):
        return [self.id, self.session, self.url, self.date, self.duration, self.streak]
    
    def to_google_sheet_list(self):
        return [self.date, self.session, self.streak, self.duration, None, None, None, f'=HYPERLINK("{self.url}", "Link")']