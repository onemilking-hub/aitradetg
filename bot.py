from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)

TOKEN = "8919833189:AAF7FG6d8FmDRJ6CpRNzPk1bTlwC8zedhhQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

WELCOME_VIDEO = "https://files.catbox.moe/4b0psz.mp4"

PLANS = {
    "plan_normal": {"name": "Normal Plan", "percent": 25, "text": "💰 <b>Normal Plan Activated</b>\n\n📊 Plan Highlights:\n• Daily Returns: 25%\n• Compounding: Not Included\n• Example Period: 30 days / 1 month projection only\n• Bot Access: Ongoing\n\n💵 Activation Requirement: Deposit $100 minimum.\n\nPlease enter your desired deposit amount:"},
    "plan_premium": {"name": "Premium Plan", "percent": 35, "text": "💰 <b>Premium Plan Activated</b>\n\n📊 Plan Highlights:\n• Daily Returns: 35%\n• Compounding: Not Included\n• Example Period: 30 days / 1 month projection only\n• Bot Access: Ongoing\n\n💵 Activation Requirement: Deposit $500 to start enjoying Premium benefits.\n\nPlease enter your desired deposit amount:"},
    "plan_diamond": {"name": "Diamond Plan", "percent": 50, "text": "💎 <b>Diamond Plan Activated</b>\n\n📊 Plan Highlights:\n• Daily Returns: 50%\n• Compounding: Available\n• Example Period: 30 days / 1 month projection only\n• Bot Access: Ongoing\n\n💵 Activation Requirement: Deposit $2000 to start enjoying Diamond benefits.\n\nPlease enter your desired deposit amount:"},
}

user_state = {}
video_shown = set()

# ==================== PROMO PORUKE SA KONFIGURACIJOM ====================
PROMO_CONFIG = [
    # Stara poruka 1
    {
        "photo": "https://files.catbox.moe/qzkf0q.jpg",
        "caption": """💥 TRADE UPDATE — +1,551.00% ROI SECURED ON NIGHTUSDT 💥

Our automated AI system just closed an explosive 100X long on NIGHTUSDT, catching the entire move with perfect precision and zero emotions.

📊 Trade Summary
• Pair: NIGHTUSDT
• Position: Long
• Leverage: 100X
• Return: +1,551.00% ROI ✅

💰 Potential Profit Examples:
• Deposit $500 → $8,255 profit
• Deposit $1,000 → $16,510 profit

✅ Instant withdrawals — profits always available
✅ Thousands of users earn daily from these automated trades

⚡️ The next high-ROI setup is already loading…
Every minute you wait is another missed 1,000%+ move.

👉 Make your deposit now and let the bot catch the next trade automatically.""",
        "delay_minutes": 1,   # 1 minut posle captcha
        "repeat": 1
    },
    # Stara poruka 2
    {
        "photo": "https://files.catbox.moe/ppftvb.jpg",
        "caption": """🎉 CONGRATULATIONS — YOU’VE BEEN RANDOMLY SELECTED OUT OF 230,000 USERS 🎉

Your account has just been awarded a limited 100X DEPOSIT BONUS, active for the next 2 HOURS ONLY.

This offer is NOT available to the public — only 0.01% of users received it today.

🔥 Deposit ANY amount from $200+ and instantly receive a full 100X bonus.
No maximum. Deposit as much as you want and multiply it by 100X.

💰 Examples (100X Bonus Active):
• Deposit $200 → Get $20,000 bonus
• Deposit $500 → Get $50,000 bonus
• Deposit $1,000 → Get $100,000 bonus
• Deposit $5,000 → Get $500,000 bonus

⚡️ All bonus funds are withdrawable instantly — no fees, no restrictions.

⏳ Your window is extremely limited.
You were chosen by pure luck — once the 2-hour timer ends, this reward expires permanently.

This is a once-in-a-lifetime opportunity…
Most users will NEVER see this bonus.

🚀 PRESS DEPOSIT NOW 
Claim your 100X bonus before your spot is given to someone else.""",
        "delay_minutes": 2,
        "repeat": 1
    },
    # Nova poruka 1
    {
        "photo": "https://files.catbox.moe/8pcfqm.jpg",
        "caption": """🚨 LIMITED SPOTS – INSANE 10X MULTIPLIER OFFER JUST DROPPED! 🚨

💸 Turn Your Deposit into a Fortune — Starting from JUST $100! This is your chance to multiply your balance like never before, but you MUST act NOW. Time is running out!

Here’s what’s waiting for you:
🔥 Deposit $100 ➡️ Get $1,000 (10X)
🔥 Deposit $200 ➡️ Get $3,000 (15X)
🔥 Deposit $500 ➡️ Get $10,000 (20X)
🔥 Deposit $1000 ➡️ Get $50,000 (50X)

🧠 You've already joined the bot — now it's time to take the next step and unlock REAL GAINS!

Why You Can’t Miss This:
✅ Expires in 1 hour — Don’t wait, or it’s gone!
✅ The ones who act NOW will WIN. The rest will watch.

⚡️ $100 is all it takes to start your journey. Don't let this once-in-a-lifetime opportunity slip through your fingers!

PRESS “DEPOSIT” NOW to claim your multiplier and level up your balance before it's too late!""",
        "delay_minutes": 1,
        "repeat": 1
    },
    # Nova poruka 2
    {
        "photo": "https://files.catbox.moe/lc1z8s.jpg",
        "caption": """💥 TRADE UPDATE — +1,099.00% ROI SECURED ON ROLLUSDT 💥

Our automated AI system just closed an explosive 100X long on ROLLUSDT, catching the entire move with perfect precision and zero emotions.

📊 Trade Summary
• Pair: ROLLUSDT
• Position: Long
• Leverage: 100X
• Return: +1,099.00% ROI ✅

💰 Potential Profit Examples:
• Deposit $500 → $5,995 profit
• Deposit $1,000 → $11,990 profit

✅ Instant withdrawals — profits always available
✅ Thousands of users earn daily from these automated trades

⚡ The next high-ROI setup is already loading…
Every minute you wait is another missed 1,000%+ move.

👉 Make your deposit now and let the bot catch the next trade automatically.

💬 Press below to contact support if you have any questions.""",
        "delay_minutes": 3,
        "repeat": 2
    },
    # Nova poruka 3
    {
        "photo": "https://files.catbox.moe/pgwql9.jpg",
        "caption": """🔍 How It Works — Pure Passive Income

Our AI trading bot earns you up to 25% daily — fully automated. No charts. No effort. Just profits.

🧠 Smart AI, Real Results
Trained on 4+ years of crypto data, our bot detects patterns, tracks global news, and reacts instantly — just like a pro trader.

📊 Trades That Follow the Money
It scans 100+ top coins and Solana tokens, locking into where momentum builds.
All trades run on secure DEXs with built-in risk controls — keeping your capital safe.

⚙️ You Do Nothing. It Earns Everything.
START WITH JUST $200 — EARN $100 DAILY.
Withdraw anytime, straight to your crypto wallet. Instant, private, and safe.

🔎 Transparent From Day One
After deposit, you’ll see real-time performance: trades, accuracy, and profit.

🚀 Ready to Earn While You Sleep?
Your crypto, our AI. Let’s grow it daily.
Deposit now — and start earning today.""",
        "delay_minutes": 4,
        "repeat": 1
    },
    # Nova poruka 4
    {
        "photo": "https://files.catbox.moe/d5of20.jpg",
        "caption": """💥 TRADE UPDATE — +6,267% ROI SECURED ON SPCUSDT 💥

Our automated AI system just closed an explosive 100X long on SPCUSDT, catching the entire move with perfect precision and zero emotions.

📊 Trade Summary
• Pair: SPCUSDT
• Position: Long
• Leverage: 100X
• Return: +6,267% ROI ✅

💰 Potential Profit Examples:
• Deposit $500 → $31,835 profit
• Deposit $1,000 → $63,670 profit

✅ Instant withdrawals — profits always available
✅ Thousands of users earn daily from these automated trades

⚡ The next high-ROI setup is already loading…
Every minute you wait is another missed 1,000%+ move.

👉 Make your deposit now and let the bot catch the next trade automatically.

💬 Press below to contact support if you have any questions.""",
        "delay_minutes": 5,
        "repeat": 2
    },
    # Nova poruka 5
    {
        "photo": "https://files.catbox.moe/x9mrcr.jpg",
        "caption": """🌟 Good Morning, Users! 🌟

📈 Yesterday was phenomenal! Our bot achieved incredible success, generating an impressive +150,000% ($155,000,000) in returns! 🚀

🎉 Exciting Update: The bot delivered an outstanding 150,000% return to users yesterday, surpassing expectations and significantly growing investments. One user even earned a remarkable $2,000,000 in just one day! Stay tuned—some amazing bonuses are on the way today!

💼 Your Opportunity Awaits: Start with as little as $100, and enjoy consistent daily returns of 25%—guaranteed. This is your chance to take control and transform your financial future!

📩 Need Help? Our friendly support team is available 24/7 to answer any questions or assist with anything you need. 
📢 Join Our Community & See the Results for Yourself! Check out real user reviews and live trade updates.

💡 Make today the day you invest in your future and unlock steady growth. Start now!""",
        "delay_minutes": 6,
        "repeat": 1
    }
]

# === SLANJE PROMO PORUKA ===
async def send_promo_after_start(user_id):
    for promo in PROMO_CONFIG:
        await asyncio.sleep(promo["delay_minutes"] * 60)  # pretvara minute u sekunde
        
        for _ in range(promo["repeat"]):
            try:
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Live Support", url="https://t.me/aitradesupport")],
                    [InlineKeyboardButton(text="💰 Deposit", callback_data="deposit")]
                ])
                await bot.send_photo(
                    chat_id=user_id,
                    photo=promo["photo"],
                    caption=promo["caption"] + "\n\n💬 Press below to contact support if you have any questions.",
                    reply_markup=kb,
                    parse_mode="HTML"
                )
                await asyncio.sleep(random.randint(25, 40))  # pauza između ponavljanja
            except:
                pass

# CAPTCHA - samo dugme
async def send_captcha(chat_id, user_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Click here to prove you're human", callback_data="captcha_pass")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text="🛡️ <b>Prove you're human</b>\n\nPlease click the button below to continue.",
        reply_markup=kb,
        parse_mode="HTML"
    )

# Glavni meni (i ostatak koda ostaje identičan tvojoj skripti)
async def send_main_menu(chat_id, first_time=False):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Deposit", callback_data="deposit")],
        [InlineKeyboardButton(text="💰 Profit Calculator", callback_data="calculator")],
        [InlineKeyboardButton(text="📖 How It Works", callback_data="howitworks")],
        [InlineKeyboardButton(text="✅ User Reviews", callback_data="reviews")],
        [InlineKeyboardButton(text="👤 My Account & Balance", callback_data="account")],
        [InlineKeyboardButton(text="📞 Live Support", callback_data="livesupport")]
    ])
    
    welcome_text = ( ... )  # ostaje isti kao u tvojoj skripti

    if first_time:
        await bot.send_video(chat_id=chat_id, video=WELCOME_VIDEO, supports_streaming=True)
    
    await bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=kb, parse_mode="HTML")

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    await send_captcha(message.chat.id, user_id)

# ==================== NOVE KOMANDE (ostaju iste) ====================
# (ostatak tvog callback_handler-a, cmd_deposit, cmd_calculator itd. ostaje nepromenjen)

async def main():
    print("✅ Bot je spreman sa 7 promo poruka!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
