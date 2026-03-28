from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time

TOKEN = "8759823115:AAHUv5fTCp1NH548-xpx4mLF9VAhvl0_yJw"
ADMIN_ID = 8008313092

user_balance = {}
last_daily = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome!\nUse /daily to earn coins")

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()

    if user_id in last_daily and now - last_daily[user_id] < 86400:
        await update.message.reply_text("⏳ Already claimed today")
        return

    user_balance[user_id] = user_balance.get(user_id, 0) + 10
    last_daily[user_id] = now

    await update.message.reply_text(f"🎁 Daily: 10 coins\n💰 Total: {user_balance[user_id]}")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = user_balance.get(user_id, 0)
    await update.message.reply_text(f"💰 Balance: {bal} coins")

async def addcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Tum admin nahi ho")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Use: /addcoin user_id amount")
        return

    user_id = int(context.args[0])
    amount = int(context.args[1])

    user_balance[user_id] = user_balance.get(user_id, 0) + amount

    await update.message.reply_text(f"✅ {amount} coins added to {user_id}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("addcoin", addcoin))

print("Bot Running...")
app.run_polling()
