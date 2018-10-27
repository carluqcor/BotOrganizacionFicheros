import telebot
import json
import os

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


with open('usuarios.json') as f:
    usuarios = json.load(f)

def es_usuario(id_usuario):
    return str(id_usuario) in list(usuarios.keys())

def add_usuario(id_usuario):
    usuarios[str(id_usuario)]=[]
    with open('usuarios.json', "w") as f:
        json.dump(usuarios, f, indent=2)

def delete_user(id_usuario):
    del(usuarios[str(id_usuario)])
    with open('usuarios.json', "w") as f:
        json.dump(usuarios, f, indent=2)

# token = '669166473:AAGRjddRvsm23At_fTRKNdhv4y2wFCthjdU'

@bot.message_handler(commands = ['start'])
def handle_start(m):
    cid = m.chat.id
    if not es_usuario(cid):
        add_usuario(cid)
        bot.send_message(cid, "Bienvenido al bot!")
    else:
        bot.send_message(cid, "Ya eres usuario")

@bot.message_handler(commands = ['stop'])
def handle_stop(m):
    cid = m.chat.id
    if es_usuario(cid):
        delete_user(cid)
        bot.send_message(cid, "Usuario eliminado")
    else:
        bot.send_message(cid, "El usuario no se ha podido eliminar por que no existe")



bot.polling()
