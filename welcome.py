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
            # 🖼️ تحميل الصورة اللي عطيتي (خاصها تكون مرفوعة فـ GitHub بنفس السمية)
            background = Editor("welcome_bg.png")
            
            # 📐 أبعاد الصورة ديالك تقريباً 1024x430
            # 🖼️ تحويل صورة البروفيل لدائرة
            avatar = await load_image_async(str(member.display_avatar.url))
            profile = Editor(avatar).resize((170, 170)).circle_image()

            # ⚪ رسم دائرة بيضاء محيطة بالبروفيل فـ الجهة اليسرى
            background.ellipse((45, 130), width=180, height=180, outline="white", stroke_width=5)
            background.paste(profile, (50, 135))

            # ✍️ الخطوط (إنجليزية فقط)
            font_big = Font.poppins(size=55, variant="bold")
            font_mid = Font.poppins(size=28, variant="regular")

            # 📝 كتابة الاسم ورقم العضو بجانب الصورة
            background.text((260, 150), f"{member.name}", color="white", font=font_big)
            background.text((260, 220), f"Member #{member.guild.member_count}", color="#ffd700", font=font_mid)

            file = discord.File(fp=background.image_bytes, filename="welcome.png")

            # 💬 رسالة الترحيب (إنجليزية بالكامل)
            embed = discord.Embed(
                title="🎉 Welcome to XCharg PVP!",
                description=f"{member.mention} has just joined the server! 🚀\n\n**Member Count:** `{member.guild.member_count}`",
                color=0xFFD700 # لون ذهبي
            )
            embed.set_image(url="attachment://welcome.png")
            embed.set_footer(
                text=f"XCharg PVP • {member.guild.name}",
                icon_url=member.guild.icon.url if member.guild.icon else None
            )

            # 📤 صيفط الرسالة
            await channel.send(content=f"Welcome {member.mention}!", embed=embed, file=file)
            print(f"✅ Welcome message sent for {member.name}")

        except Exception as e:
            print(f"❌ Error in welcome: {e}")
            # رسالة احتياطية إلا وقع شي مشكل فـ الصورة
            await channel.send(f"Welcome {member.mention} to **{member.guild.name}**!")
