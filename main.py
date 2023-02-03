from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

app = ApplicationBuilder().token("5668929474:AAFqbzsH1tq42necRpTPS9tmV_A9rxFn16c").build()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(f'Hello {update.effective_user.first_name}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'/hello\n/help\n/add_contact\n/search_contact\n/print_all\n')

async def add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите фамилию, имя и номер телефона через пробел')
    
async def search_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Для поиска введите команду /search и через пробел фамилию')

async def print_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = export_data()
    print(data)
    await update.message.reply_text(data)
    
async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = list((update.message.text).split())
    print(contact)
    with open('phone.txt', 'a+', encoding='utf-8') as file:
        file.write(';'.join(contact))
        file.write(f"\n")
    await update.message.reply_text('Контакт сохранен')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = context.args
    data = export_data()
    item = search_data(word, data)
    if item != None:
        await update.message.reply_text(item)
    else:
        await update.message.reply_text('Контакт не найден')
    

def export_data():
    with open('phone.txt', 'r', encoding='utf-8') as file:
        data = []
        for line in file:
            temp = line.strip().split(';')
            data.append(temp)
    

def search_data(word, data):
    if len(data) > 0:
        for item in data:
            if word in item:
                return item
    else:
        return None

 

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("Add_Contact", add_contact))
app.add_handler(MessageHandler(filters.TEXT & ~ filters.Command, get_contact))
app.add_handler(CommandHandler("search_contact", search_contact))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("Print_all", print_all))


print('server start')
app.run_polling()
