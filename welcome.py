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
            # 🖼️ تحميل الخلفية بالمقاس الصحيح
            background = Editor("welcome_bg.png").resize((1024, 430))

            display_name = member.name
            # قص الاسم باش ما يخرجش على الصندوق
            if len(display_name) > 11: 
                display_name = display_name[:10] + "..."

            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 مقاس الصورة (210x210) مع البلاصة اللي كتوسطها فـ الدائرة الحمرا بالضبط
            profile = Editor(avatar).resize((210, 210)).circle_image()
            background.paste(profile, (70, 110)) 

            # ✍️ الخطوط
            font_name = Font.poppins(size=36, variant="bold")
            font_member = Font.poppins(size=26, variant="bold")

            # 🏷️ الاسم: استعملنا align="left" باش يبدا من مورا التاج مباشرة (X=340)
            background.text((340, 112), display_name, color="white", font=font_name, align="left")
            
            # 🔢 رقم العضو: درناه لصق حدا كلمة Member (X=535)
            background.text((535, 180), f"#{member.guild.member_count}", color="white", font=font_member, align="left")

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
