import logging
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler ,MessageHandler,filters
import requests as req
from google import genai
from PIL import Image
from io import BytesIO
client = genai.Client(api_key="AIzaSyCUFlbXaZt-DM6yjPCnjBqAP1j54OG4zHY")
chat = client.chats.create(model="gemini-2.0-flash")
img=None
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

tok='7893059527:AAH6bDlyPc2cxXbvbqjGuiX34B2pgk20wFE'
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello')

async def ai_res(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global img
    text=update.message.text
    if(img==None):
        res=chat.send_message(text)
        print(text)
        await update.message.reply_text(res.text)
    elif(img!=None):
        img = Image.open(BytesIO(img))
        res = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[img, text])
        img=None
        await update.message.reply_text(res.text)

async def img_setter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global img
    photo_file = await update.message.photo[-1].get_file()
    img_url = photo_file.file_path
    img_response = req.get(img_url)
    img = img_response.content  
    await update.message.reply_text('Image set')

if __name__ == '__main__':
    app = ApplicationBuilder().token(tok).build()
    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(filters.TEXT,ai_res)
    img_handler=MessageHandler(filters.PHOTO,img_setter)
    app.add_handler(start_handler)
    app.add_handler(text_handler)
    app.add_handler(img_handler)
    app.run_polling()
