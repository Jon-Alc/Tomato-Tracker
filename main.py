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

        last_entry_row_number = runner.get_last_entry_row_number()

        next_row = 0;
        if not last_entry_row_number:
            next_row = 3
        else:
            next_row = last_entry_row_number + 1

        
        log_messages = self.parse_messages(messages)

        last_row = next_row + len(log_messages) - 1
        update_range = f"B{next_row}:E{last_row}"

        entries = []

        for message in log_messages:
            entries.append(message.to_google_sheet_list())
        
        print(entries)
            
        if not entries:
            print("No new posts.")
            return

        runner.update_sheet(
            update_range,
            entries
        )

        runner.update_last_entry_row_number(last_row)

        # update the last-entry cell
        # reverse history() so that you get latest messages 50 at a time, then stop when an id has been found


        # runner.update_sheet(
        #     "A1:C2",
        #     [["A", "B"], ["C", "D"]],
        # )

        
        # update_range = f"A{next_row}:F{next_row}"

        # runner.update_sheet(
        #     update_range,
        #     [["1", "2", None, "4", "5", "6"]],
        # )

        return



    def parse_messages(self, messages):

        log_entries = []

        for message in messages:

            message_content = message.content
            old_day_match = re.search("^Day [0-9]+,", message_content) # ex: Day 269
            new_day_match = re.search("^Day done", message_content) # ex: Day done
            duration_match = re.search("Total time: [0-9]+ minutes", message_content)
            old_streak_match = re.search("Streak: [0-9]+", message_content) # ex: Streak: 7
            streak_broken_match = re.search("Streak broken", message_content) # ex: Streak broken

            if (old_day_match or new_day_match) and duration_match and (old_streak_match or streak_broken_match):
                
                session_indices = None
                if old_day_match:
                    session_indices = old_day_match.span()

                duration_indices = duration_match.span()

                streak_continues = not streak_broken_match
                if old_streak_match:
                    streak_indices = old_streak_match.span()
                    if message_content[streak_indices[0] + 8 : streak_indices[1]] == "1":
                        streak_continues = False

                message_id = message.id
                message_session = message_content[session_indices[0] + 4 : session_indices[1] - 1]
                message_url = message.jump_url
                message_date = message.created_at.strftime("%d %b %Y, %I:%M:%S%p")
                log_duration = message_content[duration_indices[0] + 12 : duration_indices[1] - 8]

                log_entries.append(LogEntry(message_id, message_session, message_url, message_date, log_duration, streak_continues))

        return log_entries



if __name__ == "__main__":
    main = Main()
    main.main()