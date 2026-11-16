import discord
from discord.ext import commands
import os, random, asyncio
from datetime import datetime, timezone
from welcome import setup_welcome

# ============================================================
#  ⚙️  إعدادات البوت
# ============================================================
TOKEN = os.getenv("TOKEN")
PREFIX = "!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# تحميل نظام الترحيب
setup_welcome(bot)

# ============================================================
#  📡  الأحداث
# ============================================================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"📡 Connected to {len(bot.guilds)} server(s)")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# ============================================================
#  📊  أوامر المعلومات
# ============================================================
@bot.hybrid_command(name="ping", description="سرعة البوت")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency*1000)}ms`")

@bot.hybrid_command(name="serverinfo", description="معلومات السيرفر")
async def serverinfo(ctx):
    g = ctx.guild
    e = discord.Embed(title=f"📊 {g.name}", color=discord.Color.blue())
    if g.icon: e.set_thumbnail(url=g.icon.url)
    e.add_field(name="👑 Owner", value=g.owner.mention if g.owner else "N/A", inline=True)
    e.add_field(name="👥 Members", value=g.member_count, inline=True)
    e.add_field(name="💬 Channels", value=len(g.channels), inline=True)
    e.add_field(name="🎭 Roles", value=len(g.roles), inline=True)
    e.add_field(name="📅 Created", value=g.created_at.strftime("%Y-%m-%d"), inline=True)
    e.add_field(name="🆔 ID", value=g.id, inline=True)
    e.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="userinfo", description="معلومات عضو")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    e = discord.Embed(title=f"👤 {m}", color=m.color)
    e.set_thumbnail(url=m.display_avatar.url)
    e.add_field(name="🆔 ID", value=m.id, inline=True)
    e.add_field(name="🤖 Bot", value="Yes" if m.bot else "No", inline=True)
    e.add_field(name="📅 Joined", value=m.joined_at.strftime("%Y-%m-%d") if m.joined_at else "N/A", inline=True)
    e.add_field(name="📆 Created", value=m.created_at.strftime("%Y-%m-%d"), inline=True)
    e.add_field(name="🎭 Top Role", value=m.top_role.mention, inline=True)
    await ctx.send(embed=e)

@bot.hybrid_command(name="avatar", description="صورة بروفيل عضو")
async def avatar(ctx, member: discord.Member = None):
    m = member or ctx.author
    e = discord.Embed(title=f"🖼️ {m.name}", color=m.color)
    e.set_image(url=m.display_avatar.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="banner", description="بانر عضو")
async def banner(ctx, member: discord.Member = None):
    m = member or ctx.author
    u = await bot.fetch_user(m.id)
    if not u.banner:
        return await ctx.send("❌ هذا العضو ما عندو بانر.")
    e = discord.Embed(title=f"🖼️ Banner of {m.name}", color=m.color)
    e.set_image(url=u.banner.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="botinfo", description="معلومات البوت")
async def botinfo(ctx):
    e = discord.Embed(title="🤖 XCharg PVP Bot", color=discord.Color.gold())
    e.add_field(name="Servers", value=len(bot.guilds))
    e.add_field(name="Users", value=sum(g.member_count for g in bot.guilds))
    e.add_field(name="Latency", value=f"{round(bot.latency*1000)}ms")
    e.add_field(name="Library", value=f"discord.py {discord.__version__}")
    if bot.user.avatar: e.set_thumbnail(url=bot.user.avatar.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="uptime", description="مدة تشغيل البوت")
async def uptime(ctx):
    d = datetime.now(timezone.utc) - bot.launch_time if hasattr(bot, "launch_time") else None
    await ctx.send(f"⏱️ Uptime: `{d}`" if d else "⏱️ N/A")

@bot.hybrid_command(name="membercount", description="عدد الأعضاء")
async def membercount(ctx):
    g = ctx.guild
    bots = sum(1 for m in g.members if m.bot)
    await ctx.send(f"👥 **Total:** {g.member_count} | 👤 **Humans:** {g.member_count - bots} | 🤖 **Bots:** {bots}")

@bot.hybrid_command(name="roleinfo", description="معلومات رتبة")
async def roleinfo(ctx, role: discord.Role):
    e = discord.Embed(title=f"🎭 {role.name}", color=role.color)
    e.add_field(name="ID", value=role.id)
    e.add_field(name="Members", value=len(role.members))
    e.add_field(name="Color", value=str(role.color))
    e.add_field(name="Mentionable", value=role.mentionable)
    await ctx.send(embed=e)

@bot.hybrid_command(name="channelinfo", description="معلومات قناة")
async def channelinfo(ctx, channel: discord.TextChannel = None):
    c = channel or ctx.channel
    e = discord.Embed(title=f"📺 #{c.name}", color=discord.Color.green())
    e.add_field(name="ID", value=c.id)
    e.add_field(name="Category", value=c.category.name if c.category else "N/A")
    e.add_field(name="Topic", value=c.topic or "N/A")
    e.add_field(name="Slowmode", value=f"{c.slowmode_delay}s")
    await ctx.send(embed=e)

# ============================================================
#  🛡️  أوامر الإدارة
# ============================================================
@bot.hybrid_command(name="kick", description="طرد عضو")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member}** تطرد. السبب: `{reason}`")

@bot.hybrid_command(name="ban", description="حظر عضو")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member}** تحظر. السبب: `{reason}`")

@bot.hybrid_command(name="unban", description="رفع الحظر")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: str, *, reason="No reason"):
    try:
        user = await bot.fetch_user(int(user_id))
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ **{user}** تحل الحظر عليه.")
    except Exception as e:
        await ctx.send(f"❌ خطأ: `{e}`")

@bot.hybrid_command(name="timeout", description="إسكات مؤقت (بالدقائق)")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason"):
    until = discord.utils.utcnow() + discord.timedelta(minutes=minutes) if hasattr(discord, "timedelta") else None
    from datetime import timedelta
    until = discord.utils.utcnow() + timedelta(minutes=minutes)
    await member.timeout(until, reason=reason)
    await ctx.send(f"🔇 **{member}** تسكّت لـ `{minutes}` دقيقة.")

@bot.hybrid_command(name="untimeout", description="رفع الإسكات")
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 **{member}** تحل عليه الإسكات.")

@bot.hybrid_command(name="clear", description="مسح رسائل")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 تم مسح `{amount}` رسالة.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.hybrid_command(name="slowmode", description="وضع بطيء")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Slowmode: `{seconds}s`")

@bot.hybrid_command(name="lock", description="قفل القناة")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 القناة تقفلت.")

@bot.hybrid_command(name="unlock", description="فتح القناة")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 القناة تحلات.")

@bot.hybrid_command(name="nick", description="تغيير لقب عضو")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f"✅ اللقب تبدل لـ `{nickname}`")

@bot.hybrid_command(name="addrole", description="إضافة رتبة")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ **{role.name}** تزادت لـ **{member}**")

@bot.hybrid_command(name="removerole", description="إزالة رتبة")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"✅ **{role.name}** تحيدت من **{member}**")

# ============================================================
#  🎮  أوامر الترفيه
# ============================================================
@bot.hybrid_command(name="8ball", description="كرة سحرية")
async def eightball(ctx, *, question: str):
    answers = ["✅ نعم", "❌ لا", "🤔 ربما", "💯 أكيد", "🚫 مستحيل", "😂 ما نعرف", "🎯 يقيناً", "🌧️ لا تبان"]
    e = discord.Embed(title="🎱 8Ball", color=discord.Color.purple())
    e.add_field(name="❓", value=question, inline=False)
    e.add_field(name="💬", value=random.choice(answers), inline=False)
    await ctx.send(embed=e)

@bot.hybrid_command(name="coinflip", description="رمي عملة")
async def coinflip(ctx):
    await ctx.send(f"🪙 **{random.choice(['صورة', 'كتابة'])}**")

@bot.hybrid_command(name="dice", description="رمي حجر نرد")
async def dice(ctx, sides: int = 6):
    await ctx.send(f"🎲 `{random.randint(1, sides)}` (1-{sides})")

@bot.hybrid_command(name="rps", description="حجرة ورقة مقص")
async def rps(ctx, choice: str):
    choice = choice.lower()
    if choice not in ["rock", "paper", "scissors", "حجرة", "ورقة", "مقص"]:
        return await ctx.send("❌ اختار: `rock` / `paper` / `scissors`")
    bot_choice = random.choice(["rock", "paper", "scissors"])
    wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if choice == bot_choice: r = "🤝 تعادل"
    elif wins.get(choice) == bot_choice: r = "🎉 ربحت"
    else: r = "😢 خسرت"
    await ctx.send(f"أنت: `{choice}` | بوت: `{bot_choice}`\n{r}")

@bot.hybrid_command(name="choose", description="اختيار عشوائي (فرق بـ |)")
async def choose(ctx, *, options: str):
    opts = [o.strip() for o in options.split("|") if o.strip()]
    if len(opts) < 2: return await ctx.send("❌ حط على الأقل 2 خيارات مفصولين بـ `|`")
    await ctx.send(f"🎯 **{random.choice(opts)}**")

@bot.hybrid_command(name="rate", description="تقييم شيء")
async def rate(ctx, *, thing: str):
    await ctx.send(f"⭐ تقييم **{thing}**: `{random.randint(0,10)}/10`")

@bot.hybrid_command(name="ship", description="حساب نسبة الحب")
async def ship(ctx, user1: discord.Member, user2: discord.Member = None):
    u2 = user2 or ctx.author
    p = random.randint(0, 100)
    bar = "█" * (p // 10) + "░" * (10 - p // 10)
    await ctx.send(f"💕 **{user1.name}** × **{u2.name}**\n`{bar}` **{p}%**")

@bot.hybrid_command(name="hug", description="عناق")
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🤗 **{ctx.author.name}** عانق **{member.name}**!")

@bot.hybrid_command(name="slap", description="صفعة")
async def slap(ctx, member: discord.Member):
    await ctx.send(f"👋 **{ctx.author.name}** صفع **{member.name}**! 💥")

@bot.hybrid_command(name="joke", description="نكتة")
async def joke(ctx):
    jokes = ["😂 علاش الطماطم حمرا؟ حشومة", "🤣 واش عرفتي علاش البحر مالح؟ حيت السمك كيعرق", "😆 دخل سروال لحمار… بقا محشور"]
    await ctx.send(random.choice(jokes))

@bot.hybrid_command(name="fact", description="حقيقة عشوائية")
async def fact(ctx):
    facts = ["🦈 القرش أقدم من الشجرة", "🐙 الأخطبوط عندو 3 قلوب", "🍯 العسل ما يخسرش"]
    await ctx.send(random.choice(facts))

@bot.hybrid_command(name="quote", description="اقتباس")
async def quote(ctx):
    quotes = ["✨ النجاح رحلة، ماشي محطة.", "💪 اللي كيتعب اليوم، كيرتاح غدا.", "🔥 الطموح هو الوقود."]
    await ctx.send(random.choice(quotes))

@bot.hybrid_command(name="reverse", description="قلب النص")
async def reverse(ctx, *, text: str):
    await ctx.send(f"🔁 `{text[::-1]}`")

@bot.hybrid_command(name="mock", description="سخرية من نص")
async def mock(ctx, *, text: str):
    await ctx.send("".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text)))

# ============================================================
#  🛠️  أوامر مساعدة
# ============================================================
@bot.hybrid_command(name="say", description="البوت يقول شي حاجة")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, text: str):
    await ctx.send(text)

@bot.hybrid_command(name="embed", description="إنشاء إيمبد (عنوان | وصف)")
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, content: str):
    parts = content.split("|", 1)
    title = parts[0].strip()
    desc = parts[1].strip() if len(parts) > 1 else ""
    e = discord.Embed(title=title, description=desc, color=discord.Color.gold())
    await ctx.send(embed=e)

@bot.hybrid_command(name="poll", description="استطلاع رأي")
async def poll(ctx, *, question: str):
    e = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
    e.set_footer(text=f"بواسطة {ctx.author}")
    m = await ctx.send(embed=e)
    await m.add_reaction("✅")
    await m.add_reaction("❌")

@bot.hybrid_command(name="remind", description="تذكير (بالثواني)")
async def remind(ctx, seconds: int, *, text: str):
    await ctx.send(f"⏰ غادي نذكرك بعد `{seconds}` ثانية.")
    await asyncio.sleep(seconds)
    await ctx.send(f"⏰ {ctx.author.mention} تذكير: **{text}**")

@bot.hybrid_command(name="timestamp", description="وقت الآن")
async def timestamp(ctx):
    await ctx.send(f"🕐 <t:{int(datetime.now().timestamp())}:F>")

@bot.hybrid_command(name="invite", description="دعوة البوت")
async def invite(ctx):
    url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(administrator=True))
    await ctx.send(f"🔗 [أضف البوت]({url})")

@bot.hybrid_command(name="servericon", description="أيقونة السيرفر")
async def servericon(ctx):
    if not ctx.guild.icon: return await ctx.send("❌ السيرفر ما عندوش أيقونة.")
    e = discord.Embed(color=discord.Color.blue())
    e.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="help", description="قائمة الأوامر")
async def help_cmd(ctx):
    e = discord.Embed(title="📖 أوامر XCharg PVP", color=discord.Color.gold())
    e.add_field(name="📊 Info", value="`ping` `serverinfo` `userinfo` `avatar` `banner` `botinfo` `uptime` `membercount` `roleinfo` `channelinfo`", inline=False)
    e.add_field(name="🛡️ Moderation", value="`kick` `ban` `unban` `timeout` `untimeout` `clear` `slowmode` `lock` `unlock` `nick` `addrole` `removerole`", inline=False)
    e.add_field(name="🎮 Fun", value="`8ball` `coinflip` `dice` `rps` `choose` `rate` `ship` `hug` `slap` `joke` `fact` `quote` `reverse` `mock`", inline=False)
    e.add_field(name="🛠️ Utility", value="`say` `embed` `poll` `remind` `timestamp` `invite` `servericon` `help`", inline=False)
    e.set_footer(text="كل الأوامر خدامة كـ !command وأيضا /command")
    await ctx.send(embed=e)

# ============================================================
#  ▶️  التشغيل
# ============================================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ خاصك تحط TOKEN فـ Environment Variables")
        exit(1)
    bot.launch_time = datetime.now(timezone.utc)
    bot.run(TOKEN)
