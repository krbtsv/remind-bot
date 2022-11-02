import environs

env = environs.Env()
env.read_env('.env')

BOT_TOKEN = env("BOT_TOKEN")
ADMIN_CHAT_ID = env("ADMIN_CHAT_ID")
