from telegram import Update
from telegram.ext import ContextTypes
from storage.users_db import load_users, save_users

async def register_all_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.chat_member.new_chat_member.user.id)
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
