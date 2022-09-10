import environs

env = environs.Env()
env.read_env('.env')

BOT_TOKEN = env("BOT_TOKEN")
ERROR_MESSAGE = env("ERROR_MESSAGE")
ADMIN_CHAT_ID = env("ADMIN_CHAT_ID")
