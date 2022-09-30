from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio,os
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

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
    
chatQueue = []

stopProcess = False

@app.on_message(filters.command(["ping","all"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 5:
        await message.reply("أنا أعمل بالفعل على الحد الأقصى لعدد المحادثات وهو 5 في الوقت الحالي. يرجى المحاولة مرة أخرى بعد قليل.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("-›هناك بالفعل عملية جارية في هذه الدردشة. من فضلك اضغط /stop لبدء واحدة جديدة.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = " ".join(message.command[1:])
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in app.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await app.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(1) 
              i+=10
            except IndexError:
              try:
                await app.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"-›تم ذكر العدد الإجمالي للأعضاء {i} بنجاح.\n- ›تم رفض البوتات والحسابات المحذوفة..") 
          else:
            await message.reply(f"-› تم ذكر {i} أعضاء بنجاح.\n- ›تم رفض البوتات والحسابات المحذوفة.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("-› اسف بس الادمنية يكدرون يستخدمون هالاوامر.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                    
        
@app.on_message(filters.command(["stop","cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("-› البوت لم يبدء بالعمل بالفعل..")
      else:
        stopProcess = True
        await message.reply("-› تم الايقاف.")
    else:
      await message.reply("-› اسف بس الادمنيه يكدرون يستخدمون هالامر")
  except FloodWait as e:
    await asyncio.sleep(e.value)
 
app.run()