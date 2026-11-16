import discord
from easy_pil import Editor, Canvas, load_image_async, Font
import os

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1571463915190353931"))

def setup_welcome(bot):
    @bot.event
    async def on_member_join(member: discord.Member):
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print(f"⚠️ Welcome channel {WELCOME_CHANNEL_ID} not found")
            return

        try:
            # 🎨 خلفية داكنة مع شريط ذهبي
            background = Editor(Canvas((900, 300), color="#1e1f2b"))
            background.rectangle((0, 0), width=900, height=8, fill="#ffd700")
            background.rectangle((0, 292), width=900, height=8, fill="#ffd700")

            # 🖼️ صورة بروفيل دائرية
            avatar = await load_image_async(str(member.display_avatar.url))
            profile = Editor(avatar).resize((180, 180)).circle_image()
            # حدّ أبيض حول الدائرة
            background.ellipse((55, 55), width=190, height=190, outline="white", stroke_width=4)
            background.paste(profile, (60, 60))

            # ✍️ خطوط
            font_big = Font.poppins(size=44, variant="bold")
            font_mid = Font.poppins(size=26, variant="regular")
            font_small = Font.poppins(size=18, variant="light")

            # 📝 نصوص
            background.text((280, 70), "Welcome to XCharg PVP", color="#ffd700", font=font_big)
            background.text((280, 135), f"{member.name}", color="white", font=font_mid)
            background.text((280, 180), f"Member #{member.guild.member_count}", color="#aaaaaa", font=font_small)
            background.text((280, 215), f"Joined: {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'now'}", color="#666666", font=font_small)

            file = discord.File(fp=background.image_bytes, filename="welcome.png")

            embed = discord.Embed(
                title="🎉 مرحباً بك في XCharg PVP!",
                description=f"{member.mention} نورت السيرفر! 🚀\n\n**العضو رقم:** `{member.guild.member_count}`",
                color=0xFFD700
            )
            embed.set_image(url="attachment://welcome.png")
            embed.set_footer(
                text=f"XCharg PVP • {member.guild.name}",
                icon_url=member.guild.icon.url if member.guild.icon else None
            )

            await channel.send(content=f"🎊 أهلاً {member.mention}!", embed=embed, file=file)

        except Exception as e:
            print(f"❌ Welcome error: {e}")
            try:
                await channel.send(f"🎉 أهلاً {member.mention} في **{member.guild.name}**!")
            except:
                pass
