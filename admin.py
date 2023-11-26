from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final
import dbhelper

TOKEN: Final = '6983326262:AAHAvH6anRsg11uDFsGkFxbit-OhiZSRVrg'
BOT_USERNAME = '@order_food_kict_admin_bot'
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is bot for administrator. Please proceed to choose Mahallah cafe for today by sending /choose_mahallah")

async def choose_mahallah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if '/choose_mahallah' == update.message.text:
        await update.message.reply_text("Please choose Mahallah cafeteria for today\n1. Faruq\n2. Uthman\n3. Siddiq\n4. Ali\n5. Bilal\n6. Zubair\n\nSend /choose_mahallah (mahallah_name) to choose Mahallah cafe.")
        return 0
    #reset chosen_mahallah 
    dbhelper.delete_all_row('chosen_mahallah')    

    processed = update.message.text.replace('/choose_mahallah', '')
    chosen_mahallah = processed
    dbhelper.add_row_chosen_mahallah('chosen_mahallah', chosen_mahallah)
    await update.message.reply_text("You have successfully update food for today!")

async def update_food_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '/update_food':
        await update.message.reply_text("Enter new food using the following format:\n/update_food(food_name) (food_price) (cafe_location)")
        return 0
    
    processed = update.message.text.replace('/update_food', '')
    new_food = tuple(processed.split())
    dbhelper.add_row('food', new_food)
    await update.message.reply_text(f"New food successfully added. {new_food}")
    print(f"New food successfully added. {new_food}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main():
    #Admin bot -------------------------------
    print('Starting admin bot...')
    admin_app = Application.builder().token(TOKEN).build()

    admin_app.add_handler(CommandHandler('start', start_command))
    admin_app.add_handler(CommandHandler('choose_mahallah', choose_mahallah_command))
    admin_app.add_handler(CommandHandler('update_food', update_food_command))

    admin_app.add_error_handler(error)

    print('Polling for admin bot...')
    admin_app.run_polling(poll_interval=3)

main()
    

    
