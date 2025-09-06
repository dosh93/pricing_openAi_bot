import os
import asyncio
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Хранение настроек для каждого пользователя
user_settings = defaultdict(lambda: {"input_price": 0.0, "output_price": 0.0, "rate": 0.0})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет инструкции пользователю."""
    text = (
        "Задайте цены командой /set_prices <цена_ввода_usd> <цена_вывода_usd>\n"
        "Установите курс USD→RUB командой /set_rate <курс>\n"
        "Рассчитайте стоимость командой /calc <токены_ввода> <токены_вывода>"
    )
    await update.message.reply_text(text)

async def set_prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text("Использование: /set_prices <цена_ввода_usd> <цена_вывода_usd>")
        return
    try:
        input_price = float(context.args[0])
        output_price = float(context.args[1])
    except ValueError:
        await update.message.reply_text("Цены должны быть числами")
        return
    data = user_settings[update.effective_user.id]
    data["input_price"] = input_price
    data["output_price"] = output_price
    await update.message.reply_text(
        f"Цены установлены: ввод {input_price} USD/1M, вывод {output_price} USD/1M"
    )

async def set_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Использование: /set_rate <курс_usd_к_rub>")
        return
    try:
        rate = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Курс должен быть числом")
        return
    data = user_settings[update.effective_user.id]
    data["rate"] = rate
    await update.message.reply_text(f"Курс установлен: {rate} руб. за 1 USD")

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text("Использование: /calc <токены_ввода> <токены_вывода>")
        return
    try:
        input_tokens = int(context.args[0])
        output_tokens = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Количество токенов должно быть целым числом")
        return
    data = user_settings[update.effective_user.id]
    if data["rate"] == 0 or (data["input_price"] == 0 and data["output_price"] == 0):
        await update.message.reply_text(
            "Сначала задайте цены /set_prices и курс /set_rate"
        )
        return
    input_cost_usd = input_tokens * data["input_price"] / 1_000_000
    output_cost_usd = output_tokens * data["output_price"] / 1_000_000
    total_rub = (input_cost_usd + output_cost_usd) * data["rate"]
    await update.message.reply_text(f"Стоимость: {total_rub:.2f} руб.")

async def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable not set")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_prices", set_prices))
    app.add_handler(CommandHandler("set_rate", set_rate))
    app.add_handler(CommandHandler("calc", calc))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
