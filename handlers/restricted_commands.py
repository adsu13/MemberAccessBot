from telegram import Update
from telegram.ext import ContextTypes
from storage.users_db import load_users, save_users
from storage.invites_db import load_invites, save_invites

async def restricted_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    users = load_users()
    invites = load_invites()

    if user_id not in users:
        users.append(user_id)
        save_users(users)

    if user_id not in invites:
        invites[user_id] = {"added": [], "allowed": False}
        save_invites(invites)

    added = invites[user_id]["added"]
    if len(added) >= 5:
        invites[user_id]["allowed"] = True
        save_invites(invites)
        await update.message.reply_text("✅ Comando autorizado. (Aqui você executaria a consulta real)")
    else:
        remaining = 5 - len(added)
        nick = f"@{user.username}" if user.username else user.first_name

        msg = (
            f"🚫 *Acesso negado!*\n\n"
            f"🆔 Seu ID: `{user_id}`\n"
            f"👤 Nick: {nick}\n\n"
            f"🔐 Você ainda precisa convidar *{remaining} pessoa(s)* para desbloquear os comandos do bot."
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
