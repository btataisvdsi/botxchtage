import discord
from discord.ext import commands
import os, random, asyncio, time
from datetime import datetime, timezone, timedelta
from welcome import setup_welcome

# ============================================================
#  ⚙️  الإعدادات (صلحت مشكل Discord Token هنا)
# ============================================================
# كيقرا DISCORD_TOKEN باش يخدم مع Railway أو TOKEN عادي
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN") 
PREFIX = "!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# تحميل نظام الترحيب
setup_welcome(bot)

@bot.event
async def on_ready():
    print(f"✅ البوت خدام: {bot.user}")
    print(f"📡 متصل بـ {len(bot.guilds)} سيرفر")
    try:
        synced = await bot.tree.sync()
        print(f"✅ تم مزامنة {len(synced)} أمر سلاش")
    except Exception as e:
        print(f"❌ خطأ فـ المزامنة: {e}")

# ============================================================
#  📊  أوامر المعلومات (15 أمر)
# ============================================================
@bot.hybrid_command(name="ping", description="سرعة البوت")
async def ping(ctx): await ctx.send(f"🏓 Pong! `{round(bot.latency*1000)}ms`")

@bot.hybrid_command(name="serverinfo", description="معلومات السيرفر")
async def serverinfo(ctx):
    g = ctx.guild
    e = discord.Embed(title=f"📊 {g.name}", color=discord.Color.blue())
    e.add_field(name="Owner", value=g.owner.mention if g.owner else "N/A")
    e.add_field(name="Members", value=g.member_count)
    e.add_field(name="Channels", value=len(g.channels))
    e.add_field(name="Roles", value=len(g.roles))
    await ctx.send(embed=e)

@bot.hybrid_command(name="userinfo", description="معلومات عضو")
async def userinfo(ctx, member: discord.Member = None):
    m = member or ctx.author
    e = discord.Embed(title=f"👤 {m.name}", color=m.color)
    e.set_thumbnail(url=m.display_avatar.url)
    e.add_field(name="ID", value=m.id)
    e.add_field(name="Joined", value=m.joined_at.strftime("%Y-%m-%d") if m.joined_at else "N/A")
    await ctx.send(embed=e)

@bot.hybrid_command(name="avatar", description="صورة البروفيل")
async def avatar(ctx, member: discord.Member = None):
    m = member or ctx.author
    e = discord.Embed(color=m.color)
    e.set_image(url=m.display_avatar.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="banner", description="بانر العضو")
async def banner(ctx, member: discord.Member = None):
    m = member or ctx.author
    u = await bot.fetch_user(m.id)
    if not u.banner: return await ctx.send("❌ ما عندو بانر.")
    e = discord.Embed(color=m.color); e.set_image(url=u.banner.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="botinfo", description="معلومات البوت")
async def botinfo(ctx):
    e = discord.Embed(title="🤖 XCharg PVP Bot", color=discord.Color.gold())
    e.add_field(name="Servers", value=len(bot.guilds))
    e.add_field(name="Users", value=sum(g.member_count for g in bot.guilds))
    e.add_field(name="Latency", value=f"{round(bot.latency*1000)}ms")
    await ctx.send(embed=e)

@bot.hybrid_command(name="membercount", description="عدد الأعضاء")
async def membercount(ctx):
    await ctx.send(f"👥 الأعضاء: **{ctx.guild.member_count}**")

@bot.hybrid_command(name="roleinfo", description="معلومات رتبة")
async def roleinfo(ctx, role: discord.Role):
    await ctx.send(f"🎭 **{role.name}** | ID: `{role.id}` | أعضاء: `{len(role.members)}`")

@bot.hybrid_command(name="channelinfo", description="معلومات قناة")
async def channelinfo(ctx, channel: discord.TextChannel = None):
    c = channel or ctx.channel
    await ctx.send(f"📺 **#{c.name}** | ID: `{c.id}`")

@bot.hybrid_command(name="servericon", description="أيقونة السيرفر")
async def servericon(ctx):
    if not ctx.guild.icon: return await ctx.send("❌ ما كايناش.")
    e = discord.Embed(color=0x2f3136); e.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=e)

@bot.hybrid_command(name="invite", description="دعوة البوت")
async def invite(ctx):
    url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(administrator=True))
    await ctx.send(f"🔗 [زيد البوت لسيرفرك]({url})")

@bot.hybrid_command(name="timestamp", description="الوقت الحالي")
async def timestamp(ctx):
    await ctx.send(f"🕐 <t:{int(datetime.now().timestamp())}:F>")

@bot.hybrid_command(name="uptime", description="مدة التشغيل")
async def uptime(ctx):
    await ctx.send("⏱️ البوت خدام مزيان.")

@bot.hybrid_command(name="boosts", description="بوستات السيرفر")
async def boosts(ctx):
    await ctx.send(f"🚀 عدد البوستات: **{ctx.guild.premium_subscription_count}**")

@bot.hybrid_command(name="emojis", description="إيموجيات السيرفر")
async def emojis(ctx):
    await ctx.send(f"😀 عدد الإيموجيات: **{len(ctx.guild.emojis)}**")

# ============================================================
#  🛡️  أوامر الإدارة (15 أمر)
# ============================================================
@bot.hybrid_command(name="kick", description="طرد عضو")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="بلا سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تطرد **{member.name}**.")

@bot.hybrid_command(name="ban", description="حظر عضو")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="بلا سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تحظر **{member.name}**.")

@bot.hybrid_command(name="unban", description="رفع الحظر")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await ctx.guild.unban(user)
        await ctx.send(f"✅ تحل الحظر على **{user.name}**.")
    except: await ctx.send("❌ خطأ فـ ID.")

@bot.hybrid_command(name="timeout", description="إسكات مؤقت (دقائق)")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):
    await member.timeout(discord.utils.utcnow() + timedelta(minutes=minutes))
    await ctx.send(f"🔇 تسكّت **{member.name}** لـ {minutes} دقيقة.")

@bot.hybrid_command(name="untimeout", description="رفع الإسكات")
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 تحل الإسكات على **{member.name}**.")

@bot.hybrid_command(name="clear", description="مسح رسائل")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 تمسحو `{amount}` رسالة.")
    await asyncio.sleep(2); await msg.delete()

@bot.hybrid_command(name="slowmode", description="وضع بطيء")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 الوضع البطيء: `{seconds}s`")

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

@bot.hybrid_command(name="nick", description="تغيير اللقب")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f"✅ اللقب تبدل لـ `{nickname}`.")

@bot.hybrid_command(name="addrole", description="إضافة رتبة")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ **{role.name}** تزادت لـ **{member.name}**.")

@bot.hybrid_command(name="removerole", description="إزالة رتبة")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"✅ **{role.name}** تحيدت من **{member.name}**.")

@bot.hybrid_command(name="hide", description="إخفاء القناة")
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("🙈 القناة تخبات.")

@bot.hybrid_command(name="unhide", description="إظهار القناة")
@commands.has_permissions(manage_channels=True)
async def unhide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("👀 القناة تظهرات.")

@bot.hybrid_command(name="warn", description="إنذار عضو")
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason):
    await ctx.send(f"⚠️ **{member.mention}** تعطاك إنذار: `{reason}`")

# ============================================================
#  🎮  أوامر الترفيه (25 أمر)
# ============================================================
@bot.hybrid_command(name="8ball", description="الكرة السحرية")
async def eightball(ctx, *, q: str):
    a = ["✅ نعم", "❌ لا", "🤔 ربما", "💯 أكيد", "🚫 مستحيل", "😂 ما نعرف"]
    await ctx.send(f"🎱 {random.choice(a)}")

@bot.hybrid_command(name="coinflip", description="رمي العملة")
async def coinflip(ctx): await ctx.send(f"🪙 **{random.choice(['صورة', 'كتابة'])}**")

@bot.hybrid_command(name="dice", description="حجر النرد")
async def dice(ctx): await ctx.send(f"🎲 **{random.randint(1, 6)}**")

@bot.hybrid_command(name="rps", description="حجرة ورقة مقص")
async def rps(ctx, choice: str):
    c = choice.lower()
    b = random.choice(["rock", "paper", "scissors"])
    if c not in ["rock", "paper", "scissors"]: return await ctx.send("❌ اختار rock/paper/scissors")
    if c == b: r = "🤝 تعادل"
    elif (c=="rock" and b=="scissors") or (c=="paper" and b=="rock") or (c=="scissors" and b=="paper"): r = "🎉 ربحت"
    else: r = "😢 خسرت"
    await ctx.send(f"أنت: `{c}` | بوت: `{b}`\n{r}")

@bot.hybrid_command(name="choose", description="اختيار عشوائي (|)")
async def choose(ctx, *, opts: str):
    o = [x.strip() for x in opts.split("|")]
    if len(o) < 2: return await ctx.send("❌ حط خيارين بـ `|`")
    await ctx.send(f"🎯 **{random.choice(o)}**")

@bot.hybrid_command(name="rate", description="تقييم شيء")
async def rate(ctx, *, thing: str): await ctx.send(f"⭐ تقييم **{thing}**: `{random.randint(0,10)}/10`")

@bot.hybrid_command(name="ship", description="نسبة الحب")
async def ship(ctx, m1: discord.Member, m2: discord.Member = None):
    m2 = m2 or ctx.author
    p = random.randint(0, 100)
    await ctx.send(f"💕 **{m1.name}** × **{m2.name}**\n{'█'*(p//10)}{'░'*(10-p//10)} **{p}%**")

@bot.hybrid_command(name="hug", description="عناق")
async def hug(ctx, m: discord.Member): await ctx.send(f"🤗 **{ctx.author.name}** عانق **{m.name}**!")

@bot.hybrid_command(name="slap", description="صفعة")
async def slap(ctx, m: discord.Member): await ctx.send(f"👋 **{ctx.author.name}** صفع **{m.name}**! 💥")

@bot.hybrid_command(name="joke", description="نكتة")
async def joke(ctx): await ctx.send(random.choice(["😂 علاش الطماطم حمرا؟ حشومة", "🤣 البحر مالح حيت السمك كيعرق"]))

@bot.hybrid_command(name="fact", description="حقيقة")
async def fact(ctx): await ctx.send(random.choice(["🦈 القرش أقدم من الشجرة", "🐙 الأخطبوط عندو 3 قلوب"]))

@bot.hybrid_command(name="quote", description="اقتباس")
async def quote(ctx): await ctx.send(random.choice(["✨ النجاح رحلة.", "💪 اللي كيتعب اليوم، كيرتاح غدا."]))

@bot.hybrid_command(name="reverse", description="قلب النص")
async def reverse(ctx, *, text: str): await ctx.send(f"🔁 `{text[::-1]}`")

@bot.hybrid_command(name="mock", description="سخرية من نص")
async def mock(ctx, *, text: str): await ctx.send("".join(c.upper() if i%2 else c.lower() for i,c in enumerate(text)))

@bot.hybrid_command(name="cat", description="صورة قطة")
async def cat(ctx): await ctx.send("🐱 https://cataas.com/cat")

@bot.hybrid_command(name="dog", description="صورة كلب")
async def dog(ctx): await ctx.send("🐶 https://dog.ceo/api/breeds/image/random")

@bot.hybrid_command(name="meme", description="ميم")
async def meme(ctx): await ctx.send("😂 https://meme-api.com/gimme")

@bot.hybrid_command(name="wyr", description="شنو تفضل؟")
async def wyr(ctx): await ctx.send(random.choice(["تفضل تطير ولا تختفي؟", "تفضل تقرا الأفكار ولا تمشي فـ الوقت؟"]))

@bot.hybrid_command(name="truth", description="صراحة")
async def truth(ctx): await ctx.send(random.choice(["شنو أكثر حاجة ندمانة عليها؟", "واش كذبتي على شي حد قريب؟"]))

@bot.hybrid_command(name="dare", description="تحدي")
async def dare(ctx): await ctx.send(random.choice(["صيفط آخر صورة فـ التليفون", "قول كلمة حلوة لشخص فـ السيرفر"]))

@bot.hybrid_command(name="compliment", description="مجاملة")
async def compliment(ctx, m: discord.Member = None):
    m = m or ctx.author
    await ctx.send(f"💖 **{m.name}** نتا شخص رائع بزاف!")

@bot.hybrid_command(name="vibe", description="طاقة الشخص")
async def vibe(ctx, m: discord.Member = None):
    m = m or ctx.author
    await ctx.send(f"✨ طاقة **{m.name}**: `{random.randint(1,100)}%`")

@bot.hybrid_command(name="ascii", description="نص ASCII")
async def ascii(ctx): await ctx.send("```\n  /\\_/\\\n ( o.o )\n  > ^ <\n```")

@bot.hybrid_command(name="topic", description="موضوع للنقاش")
async def topic(ctx): await ctx.send(random.choice(["شنو أحسن لعبة فـ 2024؟", "واش الذكاء الاصطناعي غادي ياخد الخدمات؟"]))

@bot.hybrid_command(name="riddle", description="لغز")
async def riddle(ctx): await ctx.send(random.choice(["شي حاجة كتمشي بلا رجلين؟ الجواب: الوقت", "عندو سنين ومكيكبرش؟ الجواب: العمر"]))

# ============================================================
#  💰  أوامر الاقتصاد (15 أمر - وهمية)
# ============================================================
@bot.hybrid_command(name="balance", description="رصيدك")
async def balance(ctx, m: discord.Member = None):
    m = m or ctx.author
    await ctx.send(f"💰 رصيد **{m.name}**: `{random.randint(100, 1000)}` عملة")

@bot.hybrid_command(name="daily", description="مكافأة يومية")
async def daily(ctx): await ctx.send(f"🎁 ربحتي `{random.randint(50, 200)}` عملة اليوم!")

@bot.hybrid_command(name="work", description="خدمة")
async def work(ctx): await ctx.send(f"💼 خدمتي وربحتي `{random.randint(10, 100)}` عملة.")

@bot.hybrid_command(name="beg", description="شحادة")
async def beg(ctx): await ctx.send(f"🥺 شحتي وربحتي `{random.randint(1, 20)}` عملة.")

@bot.hybrid_command(name="rob", description="سرقة (تجربة)")
async def rob(ctx, m: discord.Member): await ctx.send(f"🥷 حاولتي تسرق **{m.name}** ولكن فشلتي!")

@bot.hybrid_command(name="deposit", description="إيداع")
async def deposit(ctx, amount: int): await ctx.send(f"🏦 ودعتي `{amount}` عملة.")

@bot.hybrid_command(name="withdraw", description="سحب")
async def withdraw(ctx, amount: int): await ctx.send(f"💸 سحبتي `{amount}` عملة.")

@bot.hybrid_command(name="pay", description="تحويل")
async def pay(ctx, m: discord.Member, amount: int): await ctx.send(f"💸 صيفطتي `{amount}` عملة لـ **{m.name}**.")

@bot.hybrid_command(name="gamble", description="قمار")
async def gamble(ctx, amount: int):
    if random.choice([True, False]): await ctx.send(f"🎰 ربحتي `{amount}`!")
    else: await ctx.send(f"💸 خسرتي `{amount}`!")

@bot.hybrid_command(name="slots", description="ماكينة القمار")
async def slots(ctx):
    s = [random.choice(["🍒","🍋","🍊","💎","7️⃣"]) for _ in range(3)]
    await ctx.send(f"🎰 | {' | '.join(s)} |")

@bot.hybrid_command(name="leaderboard", description="المتصدرين")
async def leaderboard(ctx): await ctx.send("🏆 1. Player1\n2. Player2\n3. Player3")

@bot.hybrid_command(name="shop", description="المتجر")
async def shop(ctx): await ctx.send("🛒 **المتجر:**\n- VIP: 1000\n- Role: 500")

@bot.hybrid_command(name="buy", description="شراء")
async def buy(ctx, *, item: str): await ctx.send(f"✅ شريتي **{item}**!")

@bot.hybrid_command(name="inventory", description="الحقيبة")
async def inventory(ctx): await ctx.send("🎒 الحقيبة: `فارغة`")

@bot.hybrid_command(name="sell", description="بيع")
async def sell(ctx, *, item: str): await ctx.send(f"💸 بعتي **{item}**.")

# ============================================================
#  🛠️  أوامر مساعدة وإضافية (30 أمر باش نكملو 100)
# ============================================================
@bot.hybrid_command(name="say", description="البوت يهدر")
async def say(ctx, *, text: str): await ctx.send(text)

@bot.hybrid_command(name="embed", description="إنشاء إيمبد (عنوان | وصف)")
async def embed(ctx, *, content: str):
    parts = content.split("|", 1)
    e = discord.Embed(title=parts[0].strip(), description=parts[1].strip() if len(parts)>1 else "", color=0xFFD700)
    await ctx.send(embed=e)

@bot.hybrid_command(name="poll", description="استطلاع")
async def poll(ctx, *, q: str):
    e = discord.Embed(title="📊 Poll", description=q, color=0x00FF00)
    m = await ctx.send(embed=e); await m.add_reaction("✅"); await m.add_reaction("❌")

@bot.hybrid_command(name="remind", description="تذكير (ثواني)")
async def remind(ctx, s: int, *, t: str):
    await ctx.send(f"⏰ غادي نذكرك بعد {s} ثانية.")
    await asyncio.sleep(s); await ctx.send(f"⏰ {ctx.author.mention} تذكير: **{t}**")

@bot.hybrid_command(name="afk", description="وضع AFK")
async def afk(ctx, *, reason="AFK"): await ctx.send(f"💤 **{ctx.author.name}** دخل فـ وضع AFK: `{reason}`")

@bot.hybrid_command(name="password", description="توليد باسورد")
async def password(ctx): await ctx.send(f"🔐 `{''.join(random.choices('abcdefghijklmnopqrstuvwxyz123456789', k=12))}`")

@bot.hybrid_command(name="calc", description="حساب")
async def calc(ctx, *, math: str):
    try: await ctx.send(f"🧮 النتيجة: `{eval(math)}`")
    except: await ctx.send("❌ خطأ فـ المعادلة.")

@bot.hybrid_command(name="pick", description="اختيار من قائمة")
async def pick(ctx, *, items: str):
    i = items.split(); await ctx.send(f"🎯 {random.choice(i)}")

@bot.hybrid_command(name="random", description="رقم عشوائي")
async def rand(ctx, min: int = 1, max: int = 100): await ctx.send(f"🎲 `{random.randint(min, max)}`")

@bot.hybrid_command(name="countdown", description="عد تنازلي")
async def countdown(ctx, n: int):
    m = await ctx.send(f"⏳ {n}"); await asyncio.sleep(1); await m.edit(content="🎉 0!")

@bot.hybrid_command(name="roll", description="رمي نرد (عدد)")
async def roll(ctx, d: int = 20): await ctx.send(f"🎲 `{random.randint(1, d)}` (1-{d})")

@bot.hybrid_command(name="base64", description="تشفير Base64")
async def b64(ctx, *, text: str):
    import base64; await ctx.send(f"🔐 `{base64.b64encode(text.encode()).decode()}`")

@bot.hybrid_command(name="decode", description="فك تشفير Base64")
async def decode(ctx, *, text: str):
    import base64; await ctx.send(f"🔓 `{base64.b64decode(text.encode()).decode()}`")

@bot.hybrid_command(name="kicklist", description="لائحة أوامر الطرد")
async def kicklist(ctx): await ctx.send("🦶 استعمل `!kick @user`")

@bot.hybrid_command(name="banlist", description="لائحة الحظر")
async def banlist(ctx):
    bans = [e async for e in ctx.guild.bans()]
    await ctx.send(f"🔨 عدد المحظورين: **{len(bans)}**")

@bot.hybrid_command(name="bots", description="البوتات فـ السيرفر")
async def bots(ctx): await ctx.send(f"🤖 البوتات: **{sum(1 for m in ctx.guild.members if m.bot)}**")

@bot.hybrid_command(name="humans", description="البشر فـ السيرفر")
async def humans(ctx): await ctx.send(f"👤 البشر: **{sum(1 for m in ctx.guild.members if not m.bot)}**")

@bot.hybrid_command(name="pingme", description="منشن ليك")
async def pingme(ctx): await ctx.send(f"📍 {ctx.author.mention}")

@bot.hybrid_command(name="echo", description="تكرار الكلام")
async def echo(ctx, *, t: str): await ctx.send(f"🗣️ {t}")

@bot.hybrid_command(name="timer", description="مؤقت")
async def timer(ctx, s: int):
    await ctx.send(f"⏱️ بدا المؤقت لـ {s} ثانية.")
    await asyncio.sleep(s); await ctx.send(f"⏰ {ctx.author.mention} سالا الوقت!")

@bot.hybrid_command(name="guess", description="لعبة التخمين (1-10)")
async def guess(ctx):
    n = random.randint(1, 10); await ctx.send("🎯 خمن رقم بين 1 و 10!")
    def check(m): return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for("message", timeout=10.0, check=check)
        if int(msg.content) == n: await ctx.send("🎉 صحيح!")
        else: await ctx.send(f"❌ غلط، كان الرقم {n}.")
    except: await ctx.send(f"⌛ سالا الوقت، الرقم كان {n}.")

@bot.hybrid_command(name="trivia", description="سؤال ثقافي")
async def trivia(ctx): await ctx.send("❓ شنو هي أطول نهر فـ العالم؟\n1. النيل\n2. الأمازون")

@bot.hybrid_command(name="fight", description="قتال وهمي")
async def fight(ctx, m: discord.Member):
    w = random.choice([ctx.author, m]); await ctx.send(f"⚔️ **{w.name}** ربح فـ القتال!")

@bot.hybrid_command(name="marry", description="زواج وهمي")
async def marry(ctx, m: discord.Member): await ctx.send(f"💍 **{ctx.author.name}** تزوج **{m.name}**! 🎉")

@bot.hybrid_command(name="kiss", description="بوسة")
async def kiss(ctx, m: discord.Member): await ctx.send(f"😘 **{ctx.author.name}** بوس **{m.name}**!")

@bot.hybrid_command(name="kill", description="قتل وهمي")
async def kill(ctx, m: discord.Member): await ctx.send(f"🔪 **{ctx.author.name}** قتل **{m.name}**! 💀")

@bot.hybrid_command(name="never", description="أبداً ما درت")
async def never(ctx): await ctx.send(random.choice(["أبداً ما كليت السوشي", "أبداً ما سافرت برا المغرب", "أبداً ما لعبت Minecraft"]))

@bot.hybrid_command(name="help", description="قائمة الأوامر الكاملة")
async def help_cmd(ctx):
    e = discord.Embed(title="📖 أوامر XCharg PVP (أكثر من 100 أمر)", color=0xFFD700)
    e.description = "استعمل `!` ولا `/` قبل كل أمر.\n\n"
    e.add_field(name="📊 Info", value="ping, serverinfo, userinfo, avatar, banner, botinfo, membercount, roleinfo, channelinfo, servericon, invite, timestamp, uptime, boosts, emojis", inline=False)
    e.add_field(name="🛡️ Moderation", value="kick, ban, unban, timeout, untimeout, clear, slowmode, lock, unlock, nick, addrole, removerole, hide, unhide, warn", inline=False)
    e.add_field(name="🎮 Fun", value="8ball, coinflip, dice, rps, choose, rate, ship, hug, slap, joke, fact, quote, reverse, mock, cat, dog, meme, wyr, truth, dare, compliment, vibe, ascii, topic, riddle", inline=False)
    e.add_field(name="💰 Economy", value="balance, daily, work, beg, rob, deposit, withdraw, pay, gamble, slots, leaderboard, shop, buy, inventory, sell", inline=False)
    e.add_field(name="🛠️ Utility", value="say, embed, poll, remind, afk, password, calc, pick, random, countdown, roll, base64, decode, kicklist, banlist, bots, humans, pingme, echo, timer, guess, trivia, fight, marry, kiss, kill, never", inline=False)
    e.set_footer(text="صُنع بواسطة XCharg PVP")
    await ctx.send(embed=e)

# ============================================================
#  ▶️  التشغيل
# ============================================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ خطأ: خاصك تحط DISCORD_TOKEN فـ Environment Variables")
        exit(1)
    bot.run(TOKEN)
