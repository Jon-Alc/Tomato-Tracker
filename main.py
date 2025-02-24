from tokens import BOT_TOKEN, DAYS_OF_DEV_CHANNEL_ID
import discord
from cacher import Cacher

class MyClient(discord.Client):

    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        self.dev_log_channel = self.get_channel(DAYS_OF_DEV_CHANNEL_ID)
        print(f"Accessed {self.dev_log_channel}, getting posts...")
        
        messages = [message async for message in self.dev_log_channel.history(limit=10)]
        for message in messages:
            print(message.content)
        

    # async def on_message(self, message):
    #     print(f"Message from {message.author}: {message.content}")
    


def main():
    
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()