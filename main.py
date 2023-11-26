from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import dbhelper

TOKEN: Final = '__REDACTED__'
BOT_USERNAME: Final = '@order_food_kict_bot'
DELIVERY_FEE: Final = 1

orders = []
chosen_mahallah = dbhelper.read_table('chosen_mahallah')
chosen_mahallah = chosen_mahallah[0][0]
food_options = []
food_options_id = []


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Order Food KICT! Everyday, Motion-U will updates food options and rotate it around all Mahallah's cafe in IIUM. \n\nSend /menu to view menu for today.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Get help")

# kene buat supaya bot query ke database
async def show_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chosen_mahallah = dbhelper.read_table('chosen_mahallah')
        chosen_mahallah = chosen_mahallah[0][0]
    except:
        await update.message.reply_text("Database is not updated yet by administrator")
        return 0

    global food_options
    food_options = dbhelper.read_mahallah_food(chosen_mahallah)

    #get all food id
    for food in food_options:
        food_options_id.append(food[0])

    mahallah = chosen_mahallah
    mahallah.capitalize()
    try:
        await update.message.reply_text(f"Today's menu is coming from Mahallah {mahallah}. Here are the menu for today!")
        for food in food_options:
            await update.message.reply_text(f'{food[0]}. {food[1]} -> RM{food[2]}')

        await update.message.reply_text("Send /order to start ordering your food.\n\nFormat of order: /order(food_id) (amount)\nExample: /order 1 1")
    except:
        await update.message.reply_text("Administrator is not yet updating the menu")

async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    processed = update.message.text.replace('/order', '')
    food_id, amount = processed.split()
    food_id = int(food_id)
    amount = int(amount)
    order = {"food_id":food_id, "amount":amount}

    if food_id not in food_options_id:
        await update.message.reply_text("You are ordering food that is not available in our list")
        return 0

    orders.append(order)

    print(f'Adding order for User {user_id}. Order {order}')
    await update.message.reply_text(f'Your order is \n{orders}.')
    await update.message.reply_text(f'If you wish to add more item, send /order (id) (amount) again.\nIf you wish to close your order. send /close_order')

async def close_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not orders:
        await update.message.reply_text("You do not have any order yet..")
        return 0
    
    #buat logic untuk close order, calculate total price
    total_price = 0
    total_delivery_fee = 0
    total_food_price = 0

    for order in orders:
        food_id = order["food_id"]
        amount = order["amount"]

        #return food_options that has same food_id as ordered food
        for x in food_options:
            food_option = x if int(x[0]) == food_id else None

        food_price = food_option[2]
        total_food_price = amount * food_price
        total_delivery_fee = amount * DELIVERY_FEE
        total_price += total_food_price + total_delivery_fee

    print(f"Closing order for User {user_id}. RM{total_price}")
    await update.message.reply_text(f"Total is RM{total_price}. RM{total_food_price} for total food price and RM{total_delivery_fee} for delivery fee.")
    #NEED TO INCLUDE PAYMENT METHOD HERE
    #AFTER PAYMENT HAS BEEN VERIFIED, NEED TO UPDATE ORDERS CACHE INTO DATABASE

async def view_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    print(f"Displaying all orders for User {user_id}")

    if not orders:
        await update.message.reply_text("There is no order yet..")
        return 0
    
    await update.message.reply_text('Your order:\n')
    for order in orders:
        await update.message.reply_text(f"{order}\n")
        
async def reset_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    print(f'Resetting order for User {user_id}')
    orders.clear()
    await update.message.reply_text("Your order has been reset")


#Responses 
def handle_response(text: str) -> str:
    if 'hello' in text:
        return "Hi, may I help you?"
    else:
        return 'Sorry I cannot understand you. Refer to /help for all available commands'        

#Handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = handle_response(text)
    await update.message.reply_text(response)

# STILL NOT WORKING!!!
async def handle_receipt(update:Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download(f'photos/{user.id}_{photo_file.file_path.rsplit("/", 1)[-1]}')
    await update.message.reply_text(f'Thank you for the receipt, {user.first_name}!. Our administrator will verify the receipt and notify you later on')
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main():
    #User bot ------------------------------------
    print('Starting user bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('menu', show_menu_command))
    app.add_handler(CommandHandler('order', order_command))
    app.add_handler(CommandHandler('close_order', close_order_command))
    app.add_handler(CommandHandler('view_order', view_order_command))
    app.add_handler(CommandHandler('reset_order', reset_order_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_receipt))

    #Errors
    app.add_error_handler(error)

    #Polls the bot

    print('Polling for user bot...')
    app.run_polling(poll_interval=3)


main()



