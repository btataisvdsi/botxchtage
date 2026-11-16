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
            background = Editor("welcome_bg.png")

            display_name = member.name
            if len(display_name) > 12:
                display_name = display_name[:11] + "..."

            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 الدائرة الحمرا
            profile = Editor(avatar).resize((360, 360)).circle_image()
            background.paste(profile, (110, 205))

            # ✍️ الخطوط
            font_name = Font.poppins(size=85, variant="bold")
            font_member = Font.poppins(size=45, variant="bold")

            # 🏷️ الاسم ورقم العضو
            background.text((780, 215), display_name, color="white", font=font_name, align="left")
            background.text((800, 365), f"Member #{member.guild.member_count}", color="white", font=font_member, align="left")

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
            # 🚨 هاد السطر غادي يصيفط ليك الخطأ فـ ديسكورد باش نعرفو السبب
            await channel.send(f"⚠️ Error in welcome image: `{e}`\n{Fallback: Welcome {member.mention}!}")
