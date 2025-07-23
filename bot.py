import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, CommandHandler, ChatMemberHandler, filters

from handlers.invite_handler import handle_invites
from handlers.register_all import register_all_members
from handlers.restricted_commands import restricted_command

logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_invites))
app.add_handler(ChatMemberHandler(register_all_members, ChatMemberHandler.CHAT_MEMBER))

restricted_cmds = [
    "cpf", "nome", "telefone", "rg", "chave", "cnpj", "placa", "email",
    "empregos", "cep", "motor", "chassi", "pai", "visinhos", "funcionarios", "ip"
]

for cmd in restricted_cmds:
    app.add_handler(CommandHandler(cmd, restricted_command))

if __name__ == "__main__":
    print("🤖 Bot is running...")
    app.run_polling()
