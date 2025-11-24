
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# -----------------------------
# Command Handlers
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Indoor Soccer Bot is running. Use /help to see commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )

# Example button callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

# -----------------------------
# Main function
# -----------------------------
async def main():
    # Replace YOUR_BOT_TOKEN with your actual token
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    await app.run_polling()

# -----------------------------
# Run bot safely with existing loop
# -----------------------------
if __name__ == "__main__":
    try:
        # If an event loop is already running (e.g., Render, Jupyter)
        loop = asyncio.get_running_loop()
        loop.create_task(main())
    except RuntimeError:
        # No running loop, safe to start one
        asyncio.run(main())
