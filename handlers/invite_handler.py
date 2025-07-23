from telegram import Update
from telegram.ext import ContextTypes
from storage.invites_db import load_invites, save_invites
from storage.users_db import load_users, save_users

async def handle_invites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    inviter = update.message.from_user
    inviter_id = str(inviter.id)

    invites = load_invites()
    users = load_users()

    invites.setdefault(inviter_id, {"added": [], "allowed": False})

    for member in new_members:
        member_id = str(member.id)

        # Adiciona ao users.json
        if member_id not in users:
            users.append(member_id)

        # Atualiza lista de quem convidou quem
        if not member.is_bot and member_id != inviter_id:
            if member_id not in invites[inviter_id]["added"]:
                invites[inviter_id]["added"].append(member_id)

        # Libera o convidador se tiver 5+ convites
        if len(invites[inviter_id]["added"]) >= 5:
            invites[inviter_id]["allowed"] = True

        # 🆕 Envia mensagem personalizada de boas-vindas
        nick = f"@{member.username}" if member.username else member.first_name
        welcome_text = (
            f"👋 Seja bem-vindo(a)\n"
            f"🆔 ID: `{member_id}`\n"
            f"👤 Nick: {nick}\n\n"
            f"🔑 Adicione 5 pessoas ao grupo para desbloquear os comandos do bot."
        )
        await update.message.reply_text(welcome_text, parse_mode="Markdown")

    save_invites(invites)
    save_users(users)
