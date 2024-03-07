from aiofiles import open as async_open
from discord import ApplicationContext, Bot, Option, SlashCommandGroup
from orjson import loads

from subprocess import run, PIPE
from config import MANAGERS

from .base import GroupCog
from .schema import CogConfig


async def check_is_manager(ctx: ApplicationContext) -> bool:
    if ctx.author.id in MANAGERS:
        return True
    await ctx.respond("Permission denied")
    return False


class System(GroupCog):
    group = SlashCommandGroup(
        name="system",
        description="System commands.",
        checks=[check_is_manager],
    )
    cogs_data: dict[str, CogConfig] = {}

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        with open("cogs/cogs.json", "rb") as cogs_file:
            raw_config: dict = loads(cogs_file.read())
            self.cogs_data: dict[str, CogConfig] = {
                item[0]: CogConfig(**item[1])
                for item in raw_config.items()
            }
        for cog_path in map(
            lambda data: data.path,
            filter(
                lambda data: data.load_on_start,
                self.cogs_data.values()
            )
        ):
            self.bot.load_extension(cog_path)

    async def update_cogs_data(self):
        async with async_open("cogs/cogs.json", "rb") as cogs_file:
            self.cogs_data = loads(await cogs_file.read())

    @property
    def all_cogs(self) -> list[str]:
        return list(self.cogs_data.keys())

    @property
    def loaded_cogs(self) -> list[str]:
        return self._loaded_cogs()

    def _loaded_cogs(self, *args) -> list[str]:
        return list(filter(lambda cog_name: cog_name != "System", self.bot.cogs.keys()))

    @property
    def unloaded_cogs(self) -> list[str]:
        return self._unloaded_cogs()

    def _unloaded_cogs(self, *args) -> list[str]:
        loaded = list(self.bot.cogs.keys())
        return list(filter(lambda cog_name: cog_name not in loaded, self.all_cogs))

    @group.command(
        name="update", description="update cogs data",
    )
    async def update_cogs(self, ctx: ApplicationContext):
        await self.update_cogs_data()
        await ctx.respond("Update finished.")

    @group.command(
        name="show", description="show all cog",
    )
    async def show_cogs(self, ctx: ApplicationContext):
        def cog_format(cog_name: str) -> str:
            return "\n".join([
                cog_name,
                f"  - path: {self.cogs_data[cog_name].path}",
                f"  - status: {'loaded' if cog_name in self.loaded_cogs else 'unloaded'}",
                f"  - description: {self.cogs_data[cog_name].description}",
                ""
            ])

        await ctx.respond("```\n" + "\n".join(map(cog_format, self.all_cogs)) + "```")

    @group.command(
        name="load",
        description="load cog",
        options=[
            Option(
                str,
                name="cog_name",
                description="cog path",
                required=True,
                autocomplete=_unloaded_cogs,
            )
        ]
    )
    async def load_cog(
        self,
        ctx: ApplicationContext,
        cog_name: str
    ):
        if cog_name in self.unloaded_cogs:
            self.bot.load_extension(self.cogs_data[cog_name].path)
            await ctx.respond(f"`{cog_name}` loaded successfully.")
        elif cog_name in self.all_cogs:
            await ctx.respond(f"Load failed, `{cog_name}` has loaded.")
        else:
            await ctx.respond(f"Load failed, `{cog_name}` not found.")

    @group.command(
        name="reload",
        description="reload cog",
        options=[
            Option(
                str,
                name="cog_name",
                description="cog path",
                required=True,
                autocomplete=_loaded_cogs,
            )
        ]
    )
    async def reload_cog(
        self,
        ctx: ApplicationContext,
        cog_name: str
    ):
        if cog_name in self.loaded_cogs:
            self.bot.reload_extension(self.cogs_data[cog_name].path)
            await ctx.respond(f"`{cog_name}` reload successfully.")
        elif cog_name in self.all_cogs:
            await ctx.respond(f"Reload failed, `{cog_name}` not loaded.")
        else:
            await ctx.respond(f"Reload failed, `{cog_name}` not found.")

    @group.command(
        name="unload",
        description="unload cog",
        options=[
            Option(
                str,
                name="cog_name",
                description="cog path",
                required=True,
                autocomplete=_loaded_cogs,
            )
        ]
    )
    async def unload_cog(
        self,
        ctx: ApplicationContext,
        cog_name: str
    ):
        if cog_name in self.loaded_cogs:
            self.bot.unload_extension(self.cogs_data[cog_name].path)
            await ctx.respond(f"`{cog_name}` unloaded successfully.")
        elif cog_name in self.all_cogs:
            await ctx.respond(f"Unload failed, `{cog_name}` not loaded.")
        else:
            await ctx.respond(f"Unload failed, `{cog_name}` not found.")

    @group.command(
        name="fetch",
        description="fetch update from github"
    )
    async def fetch_update(
        self,
        ctx: ApplicationContext,
    ):
        async def update():
            r = await self.bot.loop.run_in_executor(None, lambda: run(["git", "pull"], stdout=PIPE))
            r.stdout.decode()
            await resp.edit_original_response(content="Output:\n```\n" + r.stdout.decode() + "\n```")
        resp = await ctx.respond("Update...")
        await update()


def setup(bot: Bot):
    bot.add_cog(System(bot=bot))
