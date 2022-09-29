import os
import asyncio
from pyrogram import Client,filters,enums

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
token = os.environ.get("TOKEN")
app = Client("tag", bot_token=token, api_id = api_id, api_hash = api_hash)

async def is_Admin(chat,id):
  admins = []
  async for m in app.get_chat_members(chat, filter=enums.ChatMembersFilter.ADMINISTRATORS):
    admins.append(m.user.id)
  if id in admins :
    return True
  else : 
    return False 
    
@app.on_message(filters.private)
async def private(c,msg):
  if "all" in msg.text :
    await msg.reply("• يستخدم الامر في المجموعات فقط")
    return False 
  if msg.text == "/start" :
    await msg.reply("• اهلا بك في بوت التاك \n• اضفني الي مجموعتك وقم بترقيتي الي مشرف \n• طريقه الاستخدام : \n @all او @all + الكلمه \n\n• مطوري : @jj8jjj8")
    return False 
    
    
array = []
@app.on_message(filters.regex("all") & ~filters.private)
async def num(client, message):
  chek = await is_Admin(message.chat.id,message.from_user.id)
  if chek == False :
    await message.reply("• يجب ان تكون مشرف بالمجموعه لاستخدام التاك")
    return False 
  i = 0
  txt = ''
  zz = message.text
  zz = zz.replace("all","").replace("@","")
  array.append(message.chat.id)
  async for x in app.get_chat_members(message.chat.id):
    try :
      if message.chat.id not in array :
        return False 
      i += 1
      txt += f"[{x.user.first_name}](tg://user?id={x.user.id}) "
      if i == 25 :
        await app.send_message(message.chat.id,f"{zz}\n{txt}")
        i = 0
        txt = ''
    except :
      print("err")


@app.on_message(filters.command("ايقاف", ""))
async def stop(client, message):
  if message.chat.id not in array :
     await message.reply("• التاك متوقف بالفعل")
     return False 
  if message.chat.id in array :
    array.remove(message.chat.id)
    await message.reply("• تم ايقاف التاك")
    return False




app.run()