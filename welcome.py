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
            # 🖼️ تحميل الخلفية وتصغيرها لمقاس موحد باش ما يتخربقش الشكل
            background = Editor("welcome_bg.png").resize((1024, 430))

            display_name = member.name
            # قص الاسم إلا كان طويل بزاف باش ما يخرجش على البوطون
            if len(display_name) > 11: 
                display_name = display_name[:10] + "..."

            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 مقاس الصورة (195x195) باش تدخل بالضبط وسط الدائرة الحمرا
            profile = Editor(avatar).resize((195, 195)).circle_image()
            
            # 📍 لصق الصورة فـ البلاصة الفارغة وسط الدائرة (مقاسة على 1024x430)
            background.paste(profile, (70, 115))

            # ✍️ تصغير الخطوط باش تمشي مع المقاس الجديد
            font_name = Font.poppins(size=55, variant="bold")
            font_member = Font.poppins(size=35, variant="bold")

            # 🏷️ كتابة الاسم فوق فـ البوطون اللي فيه التاج (تعديل الإحداثيات)
            background.text((330, 115), display_name, color="white", font=font_name, align="left")
            
            # 🔢 كتابة رقم العضو فـ البوطون الصغير اللي لتحت (تعديل الإحداثيات)
            background.text((450, 200), f"#{member.guild.member_count}", color="white", font=font_member, align="left")

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
