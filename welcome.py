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
            if len(display_name) > 12: 
                display_name = display_name[:11] + "..."

            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 صورة العضو فـ الدائرة الحمرا
            profile = Editor(avatar).resize((195, 195)).circle_image()
            background.paste(profile, (70, 115))

            # ✍️ الخطوط
            font_name = Font.poppins(size=38, variant="bold")
            font_member = Font.poppins(size=28, variant="bold")

            # 🏷️ الاسم: هبطتو لتحت باش يدخل فـ البوطون ديال التاج (X=460, Y=115)
            background.text((460, 115), display_name, color="white", font=font_name, align="center")
            
            # 🔢 رقم العضو: حيدتو لليمين باش ما يتبقش مع كلمة Member (X=555, Y=190)
            background.text((555, 190), f"#{member.guild.member_count}", color="white", font=font_member, align="left")

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
