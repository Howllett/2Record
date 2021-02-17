
from recordbot.meta import M2TOKEN
from recordbot.bot import RecordBot


if __name__ == "__main__":
    print(M2TOKEN)
    RecordBot.run(
        RecordBot(command_prefix="r2"),
        M2TOKEN
    )
