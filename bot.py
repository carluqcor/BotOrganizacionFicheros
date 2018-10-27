
import telebot
from telebot import types
from os import environ
import json
# from extra import *

# Declaración del bot
bot = telebot.TeleBot(environ['TELEGRAM_TOKEN'])

userStep = {}

def archivos_etiqueta(cid, etiqueta):
  if not usuarios[str(cid)]:
    return None
  else:
    archivos = {}
    for x, y in usuarios[str(cid)].items():
      if etiqueta in y['etiquetas']:
        archivos[x] = y
    return archivos

def get_user_step(cid):
  return userStep.get(str(cid))

def guardar_archivo(cid, id_archivo, nombre_archivo):
  usuarios[str(cid)][id_archivo] = {
                              'nombre_archivo': nombre_archivo,
                              'etiquetas': []}
  guardar_usuarios()
  
with open('usuarios.json') as f:
  usuarios = json.load(f)

def guardar_usuarios():
  with open('usuarios.json', "w") as f:
    json.dump(usuarios, f, indent=2)

def es_usuario(id_usuario):
  return str(id_usuario) in list(usuarios.keys())

def add_usuario(id_usuario):
  usuarios[str(id_usuario)]={}
  guardar_usuarios()
    
def delete_user(id_usuario):
  del(usuarios[str(id_usuario)])
  guardar_usuarios()
  
def borrar_archivo(cid, id_archivo):
  del(usuarios[str(cid)][id_archivo])
  guardar_usuarios()

def generar_teclado(cid):
  teclado = types.InlineKeyboardMarkup(row_width=1)
  if not usuarios[str(cid)]:
    return None
  for x,y in usuarios[str(cid)].items():
    b = types.InlineKeyboardButton(y['nombre_archivo'], callback_data='{}'.format(x))
    teclado.add(b)
  return teclado

def borrar_etiqueta(cid, id_archivo, etiqueta):
  usuarios[str(cid)][id_archivo]['etiquetas'].remove(etiqueta)
  guardar_usuarios()
  
# Declaración de los comandos
@bot.inline_handler(lambda query: True)
def inline_handler(q):
  "Función que maneja las peticiones inline devolviendo información sobre cualquier Pokémon"
  cid = q.from_user.id
  try:
    # Obtenemos el nombre del Pokémon
    uid = q.from_user.id
    etiqueta = q.query
    documentos = []
    archivos = archivos_etiqueta(cid, etiqueta)
    var = 1
    if archivos:
      for x,y in archivos.items():
        documentos.append(types.InlineQueryResultCachedDocument(str(var), x, y['nombre_archivo'], description=' '.join(y['etiquetas']), caption=' '.join(y['etiquetas']), parse_mode=''))
        var += 1
      bot.answer_inline_query(q.id, documentos, cache_time=1)
  except:
    pass

@bot.message_handler(commands=['start'])
def handle_start(m):
  cid = m.chat.id
  if not es_usuario(cid):
    add_usuario(cid)
    bot.send_message(cid, "Bienvenido al bot!")
  else:
    bot.send_message(cid, "Ya eres usuario")

@bot.message_handler(commands=['stop'])
def handle_stop(m):
  cid = m.chat.id
  if es_usuario(cid):
    delete_user(cid)
    bot.send_message(cid, "Usuario eliminado")
  else:
    bot.send_message(cid, "El usuario no se ha podido eliminar por que no existe")

@bot.message_handler(content_types=['document'])
def document_handle(m):
  cid = m.chat.id
  nombre_archivo = m.document.file_name
  id_archivo = m.document.file_id
  guardar_archivo(cid, id_archivo, nombre_archivo)
  bot.send_message(cid, "Archivo guardado!")

@bot.message_handler(commands=['del_file'])
def handle_delete_file(m):
  cid = m.chat.id
  teclado = generar_teclado(cid)
  if teclado:
    bot.send_message(cid, "Aquí tienes tus documentos, selecciona cuál quieres borrar", reply_markup=teclado)
  else:
    bot.send_message(cid, "¡Aún no has guardado ningún archivo!")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  cid = call.message.chat.id
  mid = call.message.message_id
  id_archivo = call.data
  borrar_archivo(cid, id_archivo)
  teclado = generar_teclado(cid)
  if teclado:
    bot.edit_message_text("Aquí tienes tus documentos, selecciona cuál quieres borrar", cid, mid, reply_markup=teclado)
  else:
    bot.edit_message_text("¡Borrados todos los archivos!", cid, mid)

@bot.message_handler(func=lambda m: m.reply_to_message and m.reply_to_message.document, commands=['del_tag'])
def del_tags(m):
  cid = m.chat.id
  etiquetas_a_borrar = m.text.split(' ')[1:]
  id_archivo = m.reply_to_message.document.file_id
  etiquetas = usuarios[str(cid)][id_archivo]["etiquetas"]
  for x in etiquetas_a_borrar:
    if x in etiquetas:
      bot.send_message(cid, "Etiqueta borrada correctamente!")
      borrar_etiqueta(cid, id_archivo, x)
    else:
      bot.send_message(cid, "La etiqueta no existe en este fichero o debe comenzar por #")

@bot.message_handler(func=lambda m: m.reply_to_message and m.reply_to_message.document)
def tags_handler(m):
  cid = m.chat.id
  id_archivo = m.reply_to_message.document.file_id
  etiquetas = usuarios[str(cid)][id_archivo]["etiquetas"]
  for x in m.text.split(' '):
    if x not in etiquetas and x.startswith('#'):
      usuarios[str(cid)][id_archivo]["etiquetas"].append(x)
      guardar_usuarios()
      bot.send_message(cid, "Etiquetas guardadas correctamente!")
    else:
      bot.send_message(cid, "La etiqueta debe comenzar por #")
      

@bot.message_handler(commands=['help'])
def help_handle(m):
  cid = m.chat.id
  bot.send_message(cid, "/start-Inicia el bot\n /stop-Para el bot\n Archivos: \n El bot guarda los archivos que recibe automaticamente\n /del_file-Muestra los archivos del usuario para que sean seleccionados\n /del_tag-Elimina la etiqueta asignada al archivo, esta debe empezar por #")
  

bot.polling(True)
