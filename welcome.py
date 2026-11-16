import discord
from easy_pil import Editor, load_image_async, Font
import os

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1571463915190353931"))

def setup_welcome(bot):
    @bot.event
    async def on_member_join(member: discord.Member):
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print(f"❌ Channel {WELCOME_CHANNEL_ID} not found!")
            return

        try:
            # 🖼️ تحميل الخلفية
            background = Editor("welcome_bg.png").resize((1024, 430))

            display_name = member.name
            # قص الاسم إلا كان طويل بزاف
            if len(display_name) > 11: 
                display_name = display_name[:10] + "..."

            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 كبرنا الصورة شوية لـ (215x215) وعدلنا البلاصة ديالها باش تبقى فالوسط
            profile = Editor(avatar).resize((215, 215)).circle_image()
            background.paste(profile, (62, 108))

            # ✍️ الخطوط
            font_name = Font.poppins(size=38, variant="bold")
            font_member = Font.poppins(size=28, variant="bold")

            # 🏷️ الاسم: حركناه لليمين (X=495) باش ما يتلاقاش مع التاج
            background.text((495, 115), display_name, color="white", font=font_name, align="center")
            
            # 🔢 رقم العضو: قربناه لـ كلمة Member (X=505)
            background.text((505, 180), f"#{member.guild.member_count}", color="white", font=font_member, align="left")

            file = discord.File(fp=background.image_bytes, filename="welcome.png")

            embed = discord.Embed(
                description=f"Welcome {member.mention} to **XCHARG PVP**! 🚀",
                color=0xFF0000
            )
            embed.set_image(url="attachment://welcome.png")
            
            await channel.send(embed=embed, file=file)
            print(f"✅ Welcome message sent for {member.name}")

        except Exception as e:
            print(f"❌ Error in welcome: {e}")
            await channel.send(f"⚠️ Error in welcome image: `{e}`\nFallback: Welcome {member.mention}!")
