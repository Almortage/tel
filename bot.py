import urllib
import urllib.request, json
import requests,os
from tqdm import tqdm
from colorama import Fore, init
import base64,sys
init(autoreset=True)
from telegram import *
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
)
import speedtest,traceback
import logging
from threading import Thread
from dotenv import load_dotenv
load_dotenv()
from gtts import gTTS
from io import BytesIO
admin_id = ['5089553588']
block_id=[]
import langdetect
if os.getenv('TOKEN')!=None:
    def texttosp(text):
     lang = langdetect.detect(text)
    
     audio = gTTS(text=text, lang=lang)
     audio_file = BytesIO()
     audio.write_to_fp(audio_file)
     audio_file.seek(0)
     return audio_file

    def status():
         with open('ids.txt', 'r') as f:
             count = len(f.readlines())
             bb=len(block_id)
         return f'عدد المشتركين:- {count} \n عدد المحظورين:- {bb}'

     # دالة لإضافة مشرف جديد
    def add_admin(update: Update, context: CallbackContext,message):
         context.user_data['answer'] ="1"
         user_id = update.message.text
         if user_id not in admin_id:
             admin_id.append(user_id)
             update.message.reply_text(f"تمت إضافة المستخدم بمعرف {user_id} كمشرف جديد.")
         else:
             update.message.reply_text(f"المستخدم بمعرف {user_id} موجود بالفعل كمشرف.")

     # دالة لتنزيل مشرف
    def remove_admin(update: Update, context: CallbackContext,message):
         context.user_data['answer'] ="1"
         user_id = update.message.text
         if user_id in admin_id:
             admin_id.remove(user_id)
             update.message.reply_text(f"تم تنزيل المستخدم بمعرف {user_id} من الإدارة.")
         else:
             update.message.reply_text(f"المستخدم بمعرف {user_id} غير موجود كمشرف.")


    def block(update: Update, context: CallbackContext,message):
         context.user_data['answer'] ="1"
         user_id = update.message.text
         if user_id in admin_id:
          update.message.reply_text(f"لا يمكن حظر المالك او المشرفين.")
          return 0
         if user_id not in block_id:
             block_id.append(user_id)
             update.message.reply_text(f"تمت حظر المستخدم بمعرف {user_id} من قبل الادارة.")
         else:
             update.message.reply_text(f"المستخدم بمعرف {user_id} محظور بالفعل.")

     # دالة لتنزيل مشرف
    def unblock(update: Update, context: CallbackContext,message):
         context.user_data['answer'] ="1"
         user_id = update.message.text
         if user_id in block_id:
             block_id.remove(user_id)
             update.message.reply_text(f"تم تنزيل حظر بمعرف {user_id} من قبل الإدارة.")
         else:
             update.message.reply_text(f"المستخدم بمعرف {user_id} غير محظور.")



     # دالة لإرسال رسالة اذاعة
    def cast(update: Update, context: CallbackContext,message):
         context.user_data['answer'] ="1"
         ids = []
         with open('ids.txt', 'r') as f:
             ids = f.readlines()
         for user_id in ids:
             try:
                 context.bot.send_message(chat_id=user_id.strip(), text=update.message.text)
             except Exception as e:
                 print(e)
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'تم إرسال الرسالة لـ {len(ids)} مشترك.')
    def cast2(update: Update, context: CallbackContext):
         context.user_data['answer'] ="1"
         ids = []
         with open('ids.txt', 'r') as f:
             ids = f.readlines()
         for user_id in ids:
             try:
                 context.bot.forwardMessage(user_id.strip(),update.effective_chat.id,update.message.message_id)
             except Exception as e:
                 print(e)
         context.bot.send_message(chat_id=update.effective_chat.id, text=f'تم إرسال الرسالة لـ {len(ids)} مشترك.')


    def button(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        if str(query.from_user.id) in admin_id:
                if query.data == 'cast':
                    context.bot.send_message(query.message.chat_id, 'ارسل ما تريد اذاعته')
                    context.user_data['answer'] = 'cast'
                elif query.data == 'cast2':
                    context.bot.send_message(query.message.chat_id, 'ارسل ما تريد اذاعته')
                    context.user_data['answer'] = 'cast2'
                    
                elif query.data == 't5':
                    context.bot.send_document(query.message.chat_id, open('ids.txt', 'r'))
                elif query.data == 'status':
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=status())
        
                elif query.data == 'add_admin':
                    context.user_data['answer'] = 'add_admin'
                    context.bot.send_message(query.message.chat_id, 'أدخل ايدي المستخدم الذي ترغب في إضافته كمشرف:')
                    
                elif query.data == 'remove_admin':
                    context.user_data['answer'] = 'remove_admin'
                    context.bot.send_message(query.message.chat_id, 'أدخل ايدي المستخدم الذي ترغب في تنزيله من الإدارة:')
                elif query.data == 'block':
                    context.user_data['answer'] = 'block'
                    context.bot.send_message(query.message.chat_id, 'أدخل ايدي المستخدم الذي ترغب في حظره:')
                    
                elif query.data == 'unblock':
                    context.user_data['answer'] = 'unblock'
                    context.bot.send_message(query.message.chat_id, 'أدخل ايدي المستخدم الذي ترغب في الغاء حظره:')
                    
        else:
                if query.data == '1':
                 context.bot.send_audio(
                  chat_id=query.from_user.id,
                  audio=texttosp(query.message.text)
                 )
                else:
                 query.reply_text("عذرًا، هذا الأمر مخصص للمطور فقط.")
    def pri(update: Update, context: CallbackContext):
     with open('ids.txt', 'r') as f:
        content = f.read()
        if str(update.effective_chat.id) in content:
            pass
        else:
            context.bot.send_message(int(admin_id[0]), f"""فعل شخص جديد البوت
اسم المستخدم:- <a href="tg://user?id={update.effective_chat.id}">{update.message.from_user.first_name}</a>
يوزر المستخدم:- {update.effective_chat.username}
ايدي المستخدم:- {update.effective_chat.id}""", parse_mode="HTML")
            with open('ids.txt', 'a') as f:
                f.write(f'{str(update.effective_chat.id)}\n')
     
     if update.message.text=="/start":
      if str(update.effective_chat.id) in admin_id:
       keyboard2 =[
       [InlineKeyboardButton("اذاعة بدون توجيه[📢] ", callback_data='cast'),InlineKeyboardButton("اذاعة توجيه [📢] ", callback_data='cast2')],
       [InlineKeyboardButton("اضافة ادمن [👑] ", callback_data='add_admin'),InlineKeyboardButton("مسح ادمن [⛔] ", callback_data='remove_admin')],
       [InlineKeyboardButton("حظر مستخدم",callback_data="block"),InlineKeyboardButton("الغاء حظر مستخدم",callback_data="unblock")],
       [InlineKeyboardButton("- ارسل التخزين 📥 .",callback_data="t5"),InlineKeyboardButton("احصائيات[📄] ", callback_data='status')],
       [InlineKeyboardButton("قناة البوت [👁] ", url="https://t.me/botatiiii")],
       ]

       reply_markup2 = InlineKeyboardMarkup(keyboard2)
       update.message.reply_text("لوحة الادمن", reply_markup=reply_markup2)
      elif not admin_id:
       mem_id=str(update.effective_chat.id)
       keyboard = [
              [InlineKeyboardButton("مطور البوت", url="https://t.me/hms_01"),InlineKeyboardButton("قناة المطور", url="https://t.me/botatiiii")],
             ]
       reply_markup = InlineKeyboardMarkup(keyboard)
       update.message.reply_text(f"""بوت ادمن بنل
تظهر هذه الرساله في حال كنت انت لست المطور او لم تضع ايديك
مطور بواسطة همس""", reply_markup=reply_markup)
             
     else:
      if str(context.user_data['answer'])=="cast":
       cast(update,context,update.message.text)
      elif str(context.user_data['answer'])=="add_admin":
       add_admin(update,context,update.message.text)
      elif str(context.user_data['answer'])=="remove_admin":
       remove_admin(update,context,update.message.text)
      elif str(context.user_data['answer'])=="block":
       block(update,context,update.message.text)
      elif str(context.user_data['answer'])=="unblock":
       unblock(update,context,update.message.text)
      elif str(context.user_data['answer'])=="cast2":
       cast2(update,context)
      else:
       pass
    def mentionss2(update: Update, context: CallbackContext):
     try:
      if update.message.chat.type == "private":
       pri(update,context)
      else:
       pass
     except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb_str = ''.join(traceback.format_tb(exc_traceback))
                update.message.reply_text("حدث خطأ ما\nاسم الخطأ:-"+str(e)+":"+tb_str+"\n قم بارسال الخطأ للمطور لحل المشكلة @Fixtagbot\nشكرا❤")
             

    def mentionss(update: Update, context: CallbackContext):
      
      mem_id=str(update.effective_chat.id)
      if str(mem_id) not in block_id:
       
           mentionss2(update,context)
      else:
       update.message.reply_text("انت محظور عليك تكليم المالك")

    try:
        updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    except:
        print("Invalid token exception")
        quit()
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    def user(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)
    
    user_handler = CommandHandler('user', user)
    dispatcher.add_handler(user_handler)
    from telegram.ext import MessageFilter

    class helpFilter(MessageFilter):
        def filter(self, message):
            return message.text != '/user'

    help_filter = helpFilter()
    
    def help(update: Update, context: CallbackContext):
         t = Thread(target = mentionss,args = (update,context))
         t.start()
    help_handler = MessageHandler(help_filter, help)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
else:
    print('env error')
