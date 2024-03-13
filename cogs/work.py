from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)
from crud.user import CRUDUser
from crud.bank import CRUDBank
from crud.stock import CRUDStock
from schemas import Bank, BankUpdate, UserUpdate
from .base import GroupCog, UserCog
import random

class WorkSystem(GroupCog, UserCog):
    bot: Bot
    crud_stock: CRUDStock = CRUDStock()
    crud_user: CRUDUser = CRUDUser()
    group = SlashCommandGroup(
        name="work",
        description="Work operation"
    )
    @group.command(
        name="sakinu_ruigao_9487",
        description="幫高睿屬實有料股份有限公司工作",
    )
    async def sakinu_ruigao_9487(self,ctx: ApplicationContext):
        
        now_stock = (await self.crud_stock.get_by_code('ruigao')).price
        salary = round(random.uniform(0,now_stock / 5))
        USERDATA = await self.crud_user.get_by_user_id(ctx.author.id)
        new_data = UserUpdate(money=USERDATA.money+salary)
        await self.crud_user.update_by_user_id(ctx.author.id,new_data)
        await ctx.respond(f'你幫高睿屬實有料股份有限公司工作獲得了 {salary} 元，由於此公司為民營事業，這一份薪水會由你的老闆，高睿支付\n不過因為工程師還沒寫好，所以暫時由國家支付')
        
def setup(bot: Bot):
    bot.add_cog(WorkSystem(bot=bot))
