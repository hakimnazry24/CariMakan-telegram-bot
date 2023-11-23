from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import admin

TOKEN: Final = '__REDACTED__'
BOT_USERNAME: Final = '@order_food_kict_bot'
DELIVERY_FEE = 1

food_options = [
    [0, 'Nasi Ayam Penyet', 6.00],
    [1, 'Nasi Lemak', 2.70],
    [2, 'Nasi Ayam Gepuk', 6.50],
]

orders = []

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Order Food KICT! Everyday, Motion-U will updates food options and rotate it around all Mahallah's cafe in IIUM. \n\nSend /menu to view menu for today.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Get help")

async def show_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here are the menu for today!")
    for (i, food) in enumerate(food_options):
        await update.message.reply_text(f'{i}. {food[1]} -> RM{food[2]}')

    await update.message.reply_text("Send /order to start ordering your food.\n\nFormat of order: /order(food_id) (amount)\nExample: /order 1 1")

async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    processed = update.message.text.replace('/order', '')
    order = processed.split()
    food_id = int(order[0])

    if food_id >= len(food_options):
        print(f"error: User {user_id} is ordering non-existing food")
        await update.message.reply_text('You are ordering food that is not in the menu!.\n\nSend /menu to get menu')
        return 0

    orders.append(order)

    print(f'Adding order for User {user_id}. Order {order}')
    await update.message.reply_text(f'Your order is \n{orders}.')
    await update.message.reply_text(f'If you wish to add more item, send /order (id) (amount) again.\nIf you wish to close your order. send /close_order')

async def close_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not orders:
        await update.message.reply_text("You do not have any order yet..")
        return 0
        
    user_id = update.message.from_user.id
    total_food_price = 0
    total_delivery_fee = 0
    total_price = 0
    total_amount = 0
    for order in orders:
        food_id = int(order[0])
        amount = int(order[1])
        total_amount += amount
        price_per_food = food_options[food_id][2]
        total_food_price += price_per_food * amount
    total_delivery_fee = DELIVERY_FEE * total_amount
    total_price = total_food_price + total_delivery_fee

    print(f"Total price User {user_id} is RM{total_price}")
    await update.message.reply_text(f'Total price is RM{total_price}. (RM{total_food_price} for food and RM{total_delivery_fee} for delivery).\n\nRM{DELIVERY_FEE} is charged for each food.\n\nPlease proceed to payment on the following account\n154053616718 Maybank Muhammad Hakim\nPlease screenshot the receipt and sent it here.')

async def view_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Displaying all orders...")
    if not orders:
        await update.message.reply_text("There is no order yet..")
        return 0
    
    view_order_text = ''
    for order in orders:
        food_id = int(order[0])
        amount = order[1]
        food_name = food_options[food_id][1]
        view_order_text += food_name + ' Amount: ' + amount
    await update.message.reply_text(f'{view_order_text}')


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

if __name__ == '__main__':
    print('Starting bot...')
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
    print('Polling...')
    app.run_polling(poll_interval=3)
