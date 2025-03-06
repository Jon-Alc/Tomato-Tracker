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

        # Get posts that have already been recorded; they will be how we know we stopped
        cached_ids = self.cacher.read_ids()

        # Get posts via history(); the moment we run into a post whose id was cached, we know to stop fetching
        new_messages = []
        new_ids = []

        incoming_messages = [message async for message in self.dev_log_channel.history(limit=1000)]

        for message in incoming_messages:

            id_string = str(message.id)

            if id_string in cached_ids:
                break

            new_ids.append(id_string)
            new_messages.append(message)
        
        self.cacher.add_ids(new_ids)
        return new_messages[::-1]

    

    async def close(self):
        print("Logging off Discord...")
        await Client.close(self)
        print("Terminated connection to Discord!")
        return