from private.tokens import BOT_TOKEN, DAYS_OF_DEV_CHANNEL_ID
from discord import Intents
from discordclient import DiscordClient
from cacher import Cacher
from logentry import LogEntry
from googlerunner import GoogleRunner
import re


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

        runner = GoogleRunner()
        next_row = runner.get_last_entry_row_number() + 1

        if not next_row:
            next_row = 3

        # messages = await client.get_messages()
        # await client.close()

        # log_messages = await self.parse_messages(messages)

        # for message in log_messages:
        #     print(message)

        # update_range = f"A{next_row}:F{len(log_messages)}"
        update_range = f"A{next_row}:F{next_row}"

        runner.update_sheet(
            update_range,
            "USER_ENTERED",
            [["1", "2", None, "4", "5", "6"]],
        )

        # use batch update
        # update the last-entry cell


        # runner.update_sheet(
        #     "A1:C2",
        #     "USER_ENTERED",
        #     [["A", "B"], ["C", "D"]],
        # )

        return

    async def parse_messages(self, messages):

        log_entries = []

        for message in messages:

            message_content = message.content
            day_match = re.search("^Day [0-9]+,", message_content)

            if day_match:
                
                duration_match = re.search("Total time: [0-9]+ minutes", message_content)
                duration_indices = duration_match.span()
                streak_match = re.search("Streak: [0-9]+", message_content)
                streak_indices = streak_match.span()

                message_id = message.id
                message_url = message.jump_url
                message_date = message.created_at
                log_duration = message_content[duration_indices[0] + 12 : duration_indices[1]]
                log_streak = message_content[streak_indices[0] + 8 : streak_indices[1]]

                log_entries.append(LogEntry(message_id, message_url, message_date, log_duration, log_streak))

        return log_entries


if __name__ == "__main__":
    main = Main()
    main.main()