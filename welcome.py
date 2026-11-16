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
            # 🖼️ تحميل الخلفية الجديدة
            background = Editor("welcome_bg.png")

            # ✂️ تحديد الاسم (إلا كان طويل بزاف كنقصوه باش ما يخرجش على البوطون)
            display_name = member.name
            if len(display_name) > 12:
                display_name = display_name[:11] + "..."

            # 🖼️ تحميل صورة البروفيل
            avatar = await load_image_async(str(member.display_avatar.url))
            
            # 🔴 تحويل الصورة لدائرة ومقاسها باش تدخل فـ الدائرة الحمرا ديال الخلفية
            # المقاس ديال الدائرة الداخلية تقريباً 360x360
            profile = Editor(avatar).resize((360, 360)).circle_image()

            # 📍 لصق صورة البروفيل فـ الدائرة الحمرا (X=110, Y=205)
            background.paste(profile, (110, 205))

            # ✍️ الخطوط (خطوط سميكة وواضحة بحال التصميم)
            font_name = Font.poppins(size=85, variant="bold")
            font_member = Font.poppins(size=45, variant="bold")

            # 🏷️ كتابة الاسم فـ البوطون الكبير (X=780, Y=215)
            # استعملنا "center" باش يتوسط الاسم فـ البوطون
            background.text(
                (780, 215), 
                display_name, 
                color="white", 
                font=font_name,
                align="left"
            )

            # 🔢 كتابة رقم العضو فـ البوطون الصغير (X=800, Y=365)
            background.text(
                (800, 365), 
                f"Member #{member.guild.member_count}", 
                color="white", 
                font=font_member,
                align="left"
            )

            # تحويل الصورة لملف
            file = discord.File(fp=background.image_bytes, filename="welcome.png")

            # 💬 رسالة الترحيب (إنجليزية بالكامل)
            embed = discord.Embed(
                description=f"Welcome {member.mention} to **XCHARG PVP**! 🚀",
                color=0xFF0000 # لون أحمر باش يمشي مع التصميم
            )
            embed.set_image(url="attachment://welcome.png")
            
            # 📤 صيفط الرسالة
            await channel.send(embed=embed, file=file)
            print(f"✅ Welcome message sent for {member.name}")

        except Exception as e:
            print(f"❌ Error in welcome: {e}")
            await channel.send(f"Welcome {member.mention} to **{member.guild.name}**!")
