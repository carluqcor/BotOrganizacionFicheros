import telebot
import os
import json

userStep = {}
def get_user_step(cid):
    return userStep.get(str(cid))

def guardar_archivo(cid, file_id, file_name):
    usuarios[str(cid)].append({'file_id': file_id, 'file_name': file_name, 'tags':[]})
    guardar_usuarios()

def guardar_usuarios():
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=2)

with open('usuarios.json') as f:
    usuarios = json.load(f)

def es_usuario(id_usuario):
    return str(id_usuario) in list(usuarios.keys())

def add_usuario(id_usuario):
    usuarios[str(id_usuario)] = []
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=2)

token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def handle_start(m):
    cid = m.chat.id
    if not es_usuario(cid):
        add_usuario(cid)
        bot.send_message(cid, "Bienvenido al bot!")
    else:
        bot.send_message(cid, "Ya eres usuario")

@bot.message_handler(commands=['subir_archivo'])
def subir_archivo(m):
    cid = m.chat.id
    if es_usuario(cid):
        bot.send_message(cid, "Pásame el archivo a guardar")
        userStep[str(cid)] = 'subir_archivo'

@bot.message_handler(content_types='document')
def archivo_handler(m):
    cid = m.chat.id
    file_id = m.document.file_id
    file_name = m.document.file_name
    guardar_archivo(cid, file_id, file_name)
    bot.send_message(cid, "Guardado!!")

bot.polling()