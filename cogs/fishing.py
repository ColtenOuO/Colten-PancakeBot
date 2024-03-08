from discord import ApplicationContext, Bot, Member
from discord.ext.commands import Cog, slash_command

from math import log10
from random import choice, randint, random, uniform

from crud.user import CRUDUser
from schemas import User, UserUpdate


class Fishing(Cog):
    bot: Bot
    fish_list: list[str] = []
    crud_user: CRUDUser = CRUDUser()

    def __init__(self, bot):
        self.bot = bot

        # Read fish file
        with open("fish.txt", "r", encoding="utf-8") as fish_file:
            self.fish_list = list(map(
                lambda line: line.strip(),
                fish_file.readlines()
            ))

    @property
    def get_fish(self) -> str:
        return choice(self.fish_list)

    async def get_user(self, user_id: int) -> User:
        user = await self.crud_user.get_by_user_id(user_id)
        if user is None:
            user = await self.crud_user.create(User(user_id=user_id))
        return user

    @slash_command(
        name="money",
        description="查詢自己有多少錢"
    )
    async def money(
        self,
        ctx: ApplicationContext
    ):
        # Get user data
        user = await self.get_user(ctx.author.id)

        # Response
        await ctx.respond("你目前有 0 元，哈哈" if user.money == 0 else f"你目前有 {user.money} 元！")

    @slash_command(
        name="pancake",
        description="查詢你現在有幾個鬆餅"
    )
    async def pancake(
        self,
        ctx: ApplicationContext
    ):
        # Get user data
        user = await self.crud_user.get_by_user_id(ctx.author.id)
        result = user.pancake

        # Response
        await ctx.respond(
            f"你現在擁有 {result} 個鬆餅" if result >= 0
            else "為什麼你的鬆餅數量是負數？？？你是不是一直在想辦法從系統偷到更多鬆餅"
        )

    @slash_command(
        name="exp",
        description="查詢你自己的經驗值"
    )
    async def experience(
        self,
        ctx: ApplicationContext
    ):
        # Get user data
        user = await self.get_user(ctx.author.id)

        # Response
        await ctx.respond(f"你目前擁有 {user.experience} 點經驗值！你一次釣魚可以釣起 {int(log10(10 + user.experience))} 次")

    @slash_command(
        name="fishing",
        description="釣起一隻魚，目前釣起高睿的機率為 1/90 !"
    )
    async def fishing(
        self,
        ctx: ApplicationContext
    ):
        # Get user data
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        # Calculate fish data
        fish_count = int(log10(10 + user.experience))
        fish_result = []
        receive_money = 0
        for _ in range(fish_count):
            fish_length = uniform(0, 1000)
            fish_price_ratio = uniform(0.03, 1)
            fish_result.append(
                f"{format(fish_length, '.2f')}公分的{self.get_fish}"
            )
            receive_money += int(fish_length * fish_price_ratio)

        # Update DB
        user_update = UserUpdate(money=user.money + receive_money)
        await self.crud_user.update_by_user_id(user_id, user_update)

        # Response
        await ctx.respond(f"你共釣起了 {fish_count} 隻魚，他們分別是{'、'.join(fish_result)}，共獲得了 {receive_money} 元")

    @slash_command(
        name="steal",
        description="嘗試偷走某個人的錢"
    )
    async def steal(
        self,
        ctx: ApplicationContext,
        *,
        target: Member
    ):
        # Check whether author equal to target
        if ctx.author.id == target.id:
            await ctx.respond("你偷你自己幹嘛？？你結帳 +10")
            return

        # Get user data
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        target_user_id = target.id
        target_user = await self.get_user(target_user_id)

        # Check whether target user's money greater than zero
        if target_user.money <= 0:
            await ctx.respond("你想偷的人已經負債或沒有錢了！不要再偷他了QQ")
            return

        # Check whether user's money greater than zero
        if user.money < 0:
            await ctx.respond("你現在都負債了還想偷錢R")
            return

        if random() < 0.3:
            # Steal success
            # Calculate steal money and get experience
            steal_money = int(uniform(0, target_user.money / 2))
            add_experience = int(steal_money * uniform(0, 1))

            # Update user's money
            user_update = UserUpdate(
                money=user.money + steal_money,
                experience=user.experience + add_experience
            )
            await self.crud_user.update_by_user_id(user_id, user_update)

            # Update target user's money
            target_user_update = UserUpdate(
                money=target_user.money - steal_money
            )
            await self.crud_user.update_by_user_id(target_user_id, target_user_update)

            # Response
            await ctx.respond("\n".join([
                f"Successful Stealing！你偷走了 {target.mention} {steal_money} 元",
                f"由於 {ctx.author.mention} 成功偷取別人的財產，獲得了 {add_experience} 點經驗值"
            ]))
        else:
            # Steal failed
            # Calculate loss money and pancake
            loss_money = int(uniform(0, target_user.money / 5))
            add_pancake = randint(0, 10)

            # Update user's money
            user_update = UserUpdate(
                money=user.money - loss_money
            )
            await self.crud_user.update_by_user_id(user_id, user_update)

            # Update target user's pancake
            target_user_update = UserUpdate(
                pancake=target_user.pancake + add_pancake
            )
            await self.crud_user.update_by_user_id(target_user_id, target_user_update)

            # Response
            await ctx.respond("\n".join([
                f"Unsuccessful Stealing，你嘗試偷取 {target.mention} 的錢失敗，損失了 {loss_money} 元",
                f"【公告】由於 {target.mention} 遭到偷取財產失敗，因此獲得 {add_pancake} 個鬆餅"
            ]))

    @slash_command(
        name="pancake_exchange",
        description="把鬆餅拿去換錢"
    )
    async def exchange_pancake(
        self,
        ctx: ApplicationContext,
        *,
        num: int
    ):
        # Get user data
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        # Check whether user's pancake greater than exchange num
        if num > user.pancake:
            await ctx.respond("你根本沒有這麼多的鬆餅，不要以為我不知道！")
            return

        # Check whether exchange pancake equal to zero
        if num == 0:
            await ctx.respond("你沒有要換任何鬆餅那你找我幹嘛？，你結帳+10")
            return

        # Check whether exchange pancake less than zero
        if num < 0:
            await ctx.respond(f"你為什麼要輸入負數？你完蛋了，我要把你輸入的東西變成你鬆餅增加的數量，所以你的鬆餅數量增加了 {num} 個")

            # Update user's pancake
            user_update = UserUpdate(pancake=user.pancake + num)
            await self.crud_user.update_by_user_id(user_id, user_update)
            return

        # Update user's pancake and money
        user_update = UserUpdate(
            pancake=user.pancake - num,
            money=user.money + 100 * num
        )
        await self.crud_user.update_by_user_id(user_id, user_update)

        await ctx.respond(f"兌換成功！你兌換了 {num} 個鬆餅")


def setup(bot: Bot):
    bot.add_cog(Fishing(bot=bot))
