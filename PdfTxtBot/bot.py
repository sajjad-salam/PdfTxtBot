import os
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, InputMediaPhoto, Update, constants
import telegram
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackQueryHandler
from .messages import *
from .extracter import TextExtractor
from .ImageExtract import extractImg
from PdfTxtBot import messages


class PDFBot:
    def __init__(self, TOKEN: str) -> None:
        self.app = ApplicationBuilder().token(TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.__start__))
        self.app.add_handler(CommandHandler("help", self.__help__))
        self.app.add_handler(MessageHandler(filters=filters.Document.MimeType(
            'application/pdf'), callback=self.__fileHandler__))
        self.app.add_handler(MessageHandler(filters=~ filters.Document.MimeType(
            'application/pdf'), callback=self.__otherHandler__))
        self.app.add_handler(CallbackQueryHandler(self.__extract_text__))
        self.app.add_handler(MessageHandler(
            filters=filters.TEXT | filters.COMMAND, callback=self.__handler__))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(update.effective_chat.id, action=constants.ChatAction.TYPING)
        await update.message.reply_text("👋")
        await context.bot.set_my_commands([BotCommand("start", "Restart the bot"), BotCommand("help", "Help Description")])
        await context.bot.send_message(update.effective_chat.id, text=START_TEXT.format(update.effective_user.first_name), parse_mode=constants.ParseMode.HTML)

    async def __help__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text=HELPTEXT, parse_mode=constants.ParseMode.HTML)

    async def __handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text=ERRORTEXT)

    async def __fileHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton(text="Extract Text 📋", callback_data="Extract")], [
            InlineKeyboardButton(text="Get Images 📷", callback_data="Img")]]
        await update.message.reply_document(document=update.message.document, caption="Click On 👇 Extract Button to Get Text", reply_markup=InlineKeyboardMarkup(keyboard))

    async def __otherHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            filename = update.message.document.file_name.split(".")
            extension = filename[len(filename)-1]
            await update.message.reply_text(text=WRONGFILE.format(extension), parse_mode=constants.ParseMode.HTML)
        except AttributeError as e:
            await update.message.reply_text("Sorry Bot can't Read this file\n\nTry Sending the file with ```.pdf``` Extension",parse_mode=constants.ParseMode.MARKDOWN_V2)

    async def __extract_text__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        filename = r"PdfTxtBot\Docs\file"+str(update.effective_chat.id)+".pdf"
        id = update.callback_query.message.document.file_id
        name=update.callback_query.message.document.file_name.split(".")[0]+".txt"
        data = await context.bot.get_file(file_id=id)
        await data.download_to_drive(custom_path=filename)
        await context.bot.answer_callback_query(update.callback_query.id, text="Downloading.....")
        if update.callback_query.data == "Extract":
            txtfilename = r"PdfTxtBot\Docs\file" + \
                str(update.effective_chat.id)+".txt"
            txt = TextExtractor(filename=filename)
            with open(txtfilename, "w",encoding="utf-8") as f:
                f.write(txt.extract)
            try:
                await context.bot.send_chat_action(action=constants.ChatAction.UPLOAD_DOCUMENT, chat_id=update.effective_chat.id)
                await context.bot.send_media_group(chat_id=update.effective_chat.id, media=[InputMediaDocument(media=open(txtfilename, "rb"), caption="Converted Text", filename=name)])
            except telegram.error.BadRequest as bd:
                if bd.message=="File must be non-empty":
                    await update.callback_query.delete_message()
                    await update.callback_query.message.reply_text(messages.SCANFILE.format(update.effective_user.first_name))
            os.remove(txtfilename)
            os.remove(filename)
        elif update.callback_query.data == "Img":
            data = await extractImg(filename)
            jpgfile = data[0]["output_jpgfiles"]
            for files in jpgfile:
                await context.bot.send_chat_action(action=constants.ChatAction.UPLOAD_PHOTO, chat_id=update.effective_chat.id)
                try:
                    await context.bot.send_photo(update.effective_chat.id, photo=open(files, "rb"), read_timeout=50, write_timeout=50)
                except telegram.error.TimedOut as tt:
                    await context.bot.send_message(update.effective_chat.id, text="Some Errored Occurred ❗")
                os.remove(files)
            os.removedirs(f"{filename}_dir")
            os.remove(filename)
