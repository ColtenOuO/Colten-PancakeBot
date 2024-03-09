from datetime import datetime
from stock.stock import StockSystem
import discord

stocksystem = StockSystem()

class Stock1:
    def get_information(self):
        embed = discord.Embed(title="高睿屬實有料股份有限公司",
                    url="https://joeshih.com/portfolio/國立成功大學敬業校區學生宿舍",
                    colour=0x00b0f4,
                    timestamp=datetime.now())

        embed.set_author(name="目前股市")

        embed.add_field(name="公司登記地址",
                        value="國立成功大學敬業校區第一宿舍 209 號房",
                        inline=False)
        embed.add_field(name="公司資本額",
                        value="1000 萬元",
                        inline=True)
        embed.add_field(name="公司介紹",
                        value="高睿屬實有料股份有限公司成立於 2024 年 3 月，主要以發展睡眠產業為主，旗下開發的產品多數廣受市場的好評，並讓許多客戶滿意到常常說出『屬實有料』一詞而聞名。",
                        inline=False)
        embed.add_field(name="公司資本額",
                        value="1000 萬元",
                        inline=True)
        embed.add_field(name="公司負責人",
                        value="高睿",
                        inline=True)
        embed.add_field(name="目前股市狀況 ( 1 股價格)",
                        value=f"{stocksystem.get_price('1')} 元",
                        inline=False)

        embed.set_image(url="https://manage-oga.ncku.edu.tw/var/file/189/1189/img/Livingroom-Salon.jpg")

        embed.set_thumbnail(url="https://pic.pimg.tw/sobeit/114268963199_n.jpg")

        embed.set_footer(text="美麗果民主共和國",
                        icon_url="https://www.coca-cola.com/content/dam/onexp/tw/zh/home-images/brands/minutemaid/sparkling/twtc_minute%20maid_prod_orange%20juice_450ml_750x750.jpg")
        return embed