from discord import Client
from discord.ext import tasks

class DiscordClient(Client):



    def pass_dependencies(self, cacher, channel_id, main_instance):
        self.cacher = cacher
        self.channel_id = channel_id
        self.main = main_instance



    async def on_ready(self):

        if not self.cacher:
            raise AttributeError("Cacher not found: run pass_dependencies() first")

        print(f"Logged on as {self.user}!")

        # run() is blocking; return execution to main()
        await self.main.on_discord_connected(self)
        return

    
    
    async def get_messages(self):

        self.dev_log_channel = self.get_channel(self.channel_id)
        print(f"Accessed {self.dev_log_channel}, getting posts...")
        messages = await self._get_channel_posts()
        return messages



    async def _get_channel_posts(self):

        """
        1: get latest post id; this will be how we know we stopped
        2: get posts 50 at a time via history(); the moment we run into a post whose id was cached, we know to stop fetching
           - it's best to fetch in from latest to earliest, to avoid iterating over the whole cache
             | this has implications for the ordering of the spreadsheet
        3: for every post not found in the cache, find the day number, time spent, and streak
        4: post these to the spreadsheet
        5: the spreadsheet will update itself
        """

        messages = [message async for message in self.dev_log_channel.history(limit=10, oldest_first=True)]
        return messages
        # 1: get latest post id; this will be how we know we stopped
        # latest_post_id = self.dev_log_channel.last_message_id
        # print(latest_post_id)

        # print(len([message async for message in self.dev_log_channel.history(limit=50, oldest_first=True)]))
        # messages = [message async for message in self.dev_log_channel.history()]
        # for i in range(len(messages)):
        #     self.cacher.write(f"{str(messages[i].id)}\n")

    

    async def close(self):
        print("Logging off Discord...")
        await Client.close(self)
        print("Terminated connection to Discord!")
        return