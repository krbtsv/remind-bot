import environs

env = environs.Env()
env.read_env('.env')

BOT_TOKEN = env("BOT_TOKEN")
ADMIN_CHAT_ID = env("ADMIN_CHAT_ID")

FROM_TIME = env("FROM_TIME")
TO_TIME = env("TO_TIME")
REMINDER_PERIOD = env("REMINDER_PERIOD")
SLEEP_CHECK_PERIOD = env.int("SLEEP_CHECK_PERIOD")
