from datetime import datetime
from discord import Intents
import re

from private.tokens import BOT_TOKEN, DAYS_OF_DEV_CHANNEL_ID
from cacher import Cacher
from discordclient import DiscordClient
from logentry import LogEntry
from googlerunner import GoogleRunner


"""
References:
- datetime (https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
"""

class Main():

    def main(self):
        
        intents = Intents.default()
        intents.message_content = True

        cacher = Cacher()

        client = DiscordClient(intents=intents)
        client.pass_dependencies(cacher, DAYS_OF_DEV_CHANNEL_ID, self)

        client.run(BOT_TOKEN)
        # .run() is blocking; .on_ready() calls the next step in main, on_discord_connected()



    async def on_discord_connected(self, client: DiscordClient):

        messages = await client.get_messages()
        await client.close()

        self.continue_execution(messages)



    def continue_execution(self, messages):

        runner = GoogleRunner()
        next_row = runner.get_last_entry_row_number() + 1

        if not next_row:
            next_row = 3

        log_messages = self.parse_messages(messages)

        update_range = f"A{next_row}:H{next_row + len(log_messages)}"

        entries = []

        for message in log_messages:
            entries.append(message.to_google_sheet_list())
            
        runner.update_sheet(
            update_range,
            "USER_ENTERED",
            entries
        )

        # update the last-entry cell
        # reverse history() so that you get latest messages 50 at a time, then stop when an id has been found


        # runner.update_sheet(
        #     "A1:C2",
        #     "USER_ENTERED",
        #     [["A", "B"], ["C", "D"]],
        # )

        
        # update_range = f"A{next_row}:F{next_row}"

        # runner.update_sheet(
        #     update_range,
        #     "USER_ENTERED",
        #     [["1", "2", None, "4", "5", "6"]],
        # )

        return



    def parse_messages(self, messages):

        log_entries = []

        for message in messages:

            message_content = message.content
            day_match = re.search("^Day [0-9]+,", message_content)

            if day_match:
                
                session_indices = day_match.span()
                duration_match = re.search("Total time: [0-9]+ minutes", message_content)
                duration_indices = duration_match.span()
                streak_match = re.search("Streak: [0-9]+", message_content)
                streak_indices = streak_match.span()

                message_id = message.id
                message_session = message_content[session_indices[0] + 4 : session_indices[1] - 1]
                message_url = message.jump_url
                message_date = message.created_at.strftime("%d %b %Y, %I:%M:%S%p")
                log_duration = message_content[duration_indices[0] + 12 : duration_indices[1] - 8]
                log_streak = message_content[streak_indices[0] + 8 : streak_indices[1]]

                log_entries.append(LogEntry(message_id, message_session, message_url, message_date, log_duration, log_streak))

        return log_entries



if __name__ == "__main__":
    main = Main()
    main.main()