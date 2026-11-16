import discord
from easy_pil import Editor, Canvas, load_image_async, Font
import os

# الروم اللي طلبتي (كيقراه من Railway أو كيعطيه قيمة افتراضية)
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1571463915190353931"))

def setup_welcome(bot):
    @bot.event
    async def on_member_join(member: discord.Member):
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print(f"⚠️ الروم {WELCOME_CHANNEL_ID} ما لقيتوش!")
            return

        try:
            # 1. إنشاء خلفية احترافية داكنة
            background = Editor(Canvas((900, 300), color="#1e1f2b"))
            
            # خطوط ذهبية فوق وتحت
            background.rectangle((0, 0), width=900, height=8, fill="#ffd700")
            background.rectangle((0, 292), width=900, height=8, fill="#ffd700")

            # 2. جلب صورة البروفيل وتحويلها لدائرة
            avatar = await load_image_async(str(member.display_avatar.url))
            profile = Editor(avatar).resize((180, 180)).circle_image()
            
            # دائرة بيضاء محيطة بالبروفيل
            background.ellipse((55, 55), width=190, height=190, outline="white", stroke_width=4)
            
            # لصق صورة البروفيل فـ البلاصة
            background.paste(profile, (60, 60))

            # 3. الخطوط
            font_big = Font.poppins(size=44, variant="bold")
            font_mid = Font.poppins(size=26, variant="regular")
            font_small = Font.poppins(size=18, variant="light")

            # 4. كتابة النصوص
            background.text((280, 70), "Welcome to XCharg PVP", color="#ffd700", font=font_big)
            background.text((280, 135), f"{member.name}", color="white", font=font_mid)
            background.text((280, 180), f"Member #{member.guild.member_count}", color="#aaaaaa", font=font_small)

            # تحويل الصورة لملف
            file = discord.File(fp=background.image_bytes, filename="welcome.png")

            # 5. رسالة الترحيب (إيمبد + منشن)
            embed = discord.Embed(
                title="🎉 مرحباً بك في XCharg PVP!",
                description=f"{member.mention} نورت السيرفر! 🚀\n\n**أنت العضو رقم:** `{member.guild.member_count}`",
                color=0xFFD700
            )
            embed.set_image(url="attachment://welcome.png")
            embed.set_footer(
                text=f"XCharg PVP • {member.guild.name}",
                icon_url=member.guild.icon.url if member.guild.icon else None
            )

            # صيفط فـ الروم
            await channel.send(content=f"🎊 أهلاً {member.mention}!", embed=embed, file=file)

        except Exception as e:
            print(f"❌ خطأ فـ الترحيب: {e}")
            await channel.send(f"🎉 أهلاً {member.mention} في **{member.guild.name}**!")
