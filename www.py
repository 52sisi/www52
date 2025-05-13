from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler  # ← Добавлен CommandHandler!

# Конфигурация бота
BOT_TOKEN = "7800664691:AAHzL_NpX7M1M_p_CwvuLnZ33UnAAjNLEvM"  # Замените на токен от @BotFather
ADMIN_CHAT_ID = -1002536808892      # Замените на ваш chat_id (узнаётся через /id)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает сообщения анонимно"""
    if not update.message:
        return
    
    # Игнорируем команды (например, /start)
    if update.message.text and update.message.text.startswith('/'):
        return
    
    # Формируем анонимное сообщение
    forwarded_msg = f":\n\n{update.message.text or ''}"
    
    # Пересылаем фото
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=forwarded_msg
        )
    # Пересылаем видео
    elif update.message.video:
        await context.bot.send_video(
            chat_id=ADMIN_CHAT_ID,
            video=update.message.video.file_id,
            caption=forwarded_msg
        )
    # Пересылаем файлы
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=update.message.document.file_id,
            caption=forwarded_msg
        )
    # Пересылаем текст
    else:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=forwarded_msg
        )
    
    # Отправляем подтверждение отправителю
    await update.message.reply_text(" Ваше сообщение отправлено анонимно!")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /id для получения chat_id"""
    await update.message.reply_text(f"Ваш chat_id: {update.message.chat_id}")

def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчик обычных сообщений
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    # Обработчик команды /id
    app.add_handler(CommandHandler("id", get_chat_id))
    
    print("Бот запущен! Для остановки нажмите Ctrl+C")
    app.run_polling()

if __name__ == "__main__":
    main()
