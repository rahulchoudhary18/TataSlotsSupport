from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import config
import logging
from handlers.mustjoin import check_user_joined_channels, generate_join_channels_keyboard
from handlers.stats import setup_stats_handlers
from handlers.database import add_user
from handlers.broadcast import setup_broadcast

app = Client("bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    user_full_name = message.from_user.first_name
    add_user(user_id, username)
    if message.from_user.last_name:
        user_full_name += ' ' + message.from_user.last_name
    #if await check_user_joined_channels(client, user_id, config.REQUIRED_CHANNEL_IDS):
    welcome_message = (
        "**Dear valued users,**\n\n"
        "**I am delighted to announce that Tataslots will be launching our highly anticipated new platform on April 22nd.**\n\n"
        "**We're excited to offer promising opportunities with competitive compensation and benefits. If you're interested in being part of our journey,**\n\n"
        "**Join us on our official Telegram channel**\n"
        "**🔵Hurry up, join Us:**\n"
        "**https://t.me/+TByVfo7Nj2JkMDRl**\n"
        "**https://t.me/+TByVfo7Nj2JkMDRl🔥🚀**\n\n"
        "**Looking forward to welcoming you aboard.**"
    )
          
    photo_url = "https://telegra.ph/file/15946f083a45b65204c31.jpg"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact", url="https://t.me/TataslotSalina")],
        [InlineKeyboardButton("👉 vip channel 👈", url="https://t.me/+dABe2ykueyozOGQ9")],
        [InlineKeyboardButton("👉 Gift codes 👈", url="https://t.me/TataslotsGift")]
    ])
    await client.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=welcome_message,
        reply_markup=reply_markup
    )
        #await message.reply_text(welcome_message, reply_markup=reply_markup)
    #else:
        #join_channels_message = (
         #   "**😎To use the BOT 🤖  you must join the below channels otherwise you can't access the bot**\n\n"
        # )
       # reply_markup = generate_join_channels_keyboard()
       # await message.reply_text(join_channels_message, reply_markup=reply_markup)

async def on_callback_query(client, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    if data == "check_joined":
        if await check_user_joined_channels(client, callback_query.from_user.id, config.REQUIRED_CHANNEL_IDS):
            await callback_query.message.edit(
                "Thank you for joining the channels! How can I assist you today?",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Get Started", callback_data="get_started")]
                    ]
                )
            )
        else:
            await callback_query.answer("Please join all required channels first.", show_alert=True)

    elif data == "get_started":
        welcome_message = (
            "**Dear valued users,**\n\n"
            "**I am delighted to announce that Tataslots will be launching our highly anticipated new platform on April 22nd.**\n\n"
            "**We're excited to offer promising opportunities with competitive compensation and benefits. If you're interested in being part of our journey,**\n\n"
            "**Join us on our official Telegram channel**\n"
            "**🔵Hurry up, join Us:**\n"
            "**https://t.me/+TByVfo7Nj2JkMDRl**\n"
            "**https://t.me/+TByVfo7Nj2JkMDRl🔥🚀**\n\n"
            "**Looking forward to welcoming you aboard.**"
        )
          
        photo_url = "https://telegra.ph/file/a3852757146a2c0fcc184.jpg"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Contact", url="https://t.me/TataslotSalina")],
            [InlineKeyboardButton("👉 vip channel 👈", url="https://t.me/+dABe2ykueyozOGQ9")],
            [InlineKeyboardButton("👉 Gift codes 👈", url="https://t.me/TataslotsGift")]
        ])
        await client.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=welcome_message,
            reply_markup=reply_markup
        )

app.add_handler(MessageHandler(start, filters.command("start")))
app.add_handler(CallbackQueryHandler(on_callback_query))
setup_stats_handlers(app)
setup_broadcast(app)

async def start_bot():
    print(">> Bot Starting")
    await app.start()
    print(">> Bot Started - Press CTRL+C to exit")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_bot())
    finally:
        loop.close()
        
