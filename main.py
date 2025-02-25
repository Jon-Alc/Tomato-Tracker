from private.tokens import BOT_TOKEN, DAYS_OF_DEV_CHANNEL_ID
from discord import Intents
from discordclient import DiscordClient
from cacher import Cacher
    


def main():
    
    intents = Intents.default()
    intents.message_content = True

    cacher = Cacher()

    client = DiscordClient(intents=intents)
    client.pass_dependencies(cacher, DAYS_OF_DEV_CHANNEL_ID)

    client.run(BOT_TOKEN)



if __name__ == "__main__":
    main()