import panel
import scheduler
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from constants import PAYMENT_FILE

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


def bytes_to_gb(b):
    return round(b / 1024 / 1024 / 1024, 4)


async def traffic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    panel.login()

    data = panel.get_inbounds()
    print(data)

    inbound = data["obj"][0]

    up = inbound["up"]
    down = inbound["down"]

    total = up + down

    msg = f"""
Общий трафик inbound за месяц

Upload: {bytes_to_gb(up)} GB
Download: {bytes_to_gb(down)} GB
Total: {bytes_to_gb(total)} GB
"""

    await update.message.reply_text(msg)

async def alltime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    panel.login()

    data = panel.get_inbounds()

    inbound = data["obj"][0]

    alltime = inbound["allTime"]

    msg = f"All time traffic: {bytes_to_gb(alltime)} GB"

    await update.message.reply_text(msg)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    panel.login()

    panel.reset_traffic()

    await update.message.reply_text("Traffic reset")


async def setday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setday 5")
        return

    day = context.args[0]

    if not day.isdigit() or int(day) < 1 or int(day) > 31:
        await update.message.reply_text("Please enter a valid day (1-31).")
        return

    day = int(day)

    with open(PAYMENT_FILE, "w") as f:
        f.write(str(day))

    os.environ["PAYMENT_DAY"] = str(day)

    await update.message.reply_text(f"Payment day set to {day}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
Команды:

/traffic — трафик за месяц
/alltime — общий трафик
/reset — сбросить трафик
/setday — установить день оплаты
"""

    await update.message.reply_text(msg)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("traffic", traffic))
app.add_handler(CommandHandler("alltime", alltime))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("setday", setday))

app.run_polling()