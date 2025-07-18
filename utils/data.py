import os
import discord
from utils import permissions, default
from utils.config import Config
from utils.db import Database
from discord.ext.commands import AutoShardedBot, DefaultHelpCommand


class DiscordBot(AutoShardedBot):
    def __init__(self, config: Config, prefix: list[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.config = config
        self.db = Database(self.config)

    async def setup_hook(self):
        # Initialize database connection pool
        try:
            await self.db.init_pool()
        except Exception as e:
            print(f"⚠️ WARNING: Failed to connect to MySQL: {e}")

        # Load all cogs from the cogs directory
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    await self.load_extension(f"cogs.{name}")
                    print(f"✅ Loaded cog: {name}")
                except Exception as e:
                    print(f"❌ Failed to load cog: {name}\n{e}")

    async def on_message(self, msg: discord.Message):
        if not self.is_ready() or msg.author.bot or \
           not permissions.can_handle(msg, "send_messages"):
            return
        await self.process_commands(msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=default.CustomContext)
        await self.invoke(ctx)


class HelpFormat(DefaultHelpCommand):
    def get_destination(self, no_pm: bool = False):
        return self.context.channel if no_pm else self.context.author

    async def send_error_message(self, error: str) -> None:
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

    async def send_command_help(self, command) -> None:
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    async def send_pages(self, no_pm: bool = False) -> None:
        try:
            if permissions.can_handle(self.context, "add_reactions"):
                await self.context.message.add_reaction(chr(0x2709))
        except discord.Forbidden:
            pass

        try:
            destination = self.get_destination(no_pm=no_pm)
            for page in self.paginator.pages:
                await destination.send(page)
        except discord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send("Couldn't send help due to blocked DMs.")
