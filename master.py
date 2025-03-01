import telebot
import sqlite3
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
bot = telebot.TeleBot("8046345837:AAHt69dTU-Laf6faVrCVXI_NyqdPfqLi9QA")


#creating master.db
with sqlite3.connect('master.db') as connection:
        cursor = connection.cursor()
        Create_Table_categories = """
        CREATE TABLE IF NOT EXISTS categories(
        id integer primary key AUTOINCREMENT,    
        c_name text,
        c_counter integer
         );
        """
        cursor.execute(Create_Table_categories)


        Create_Table_message_ids = """
        CREATE TABLE IF NOT EXISTS message_ids(
        id integer primary key AUTOINCREMENT,    
        message_ids text,
        message_title text,
        message_subcategory_name integer
         );
        """
        cursor.execute(Create_Table_message_ids)


#main_keyword
m_init = InlineKeyboardButton(text="initialize new category", callback_data="m_init")
m_get = InlineKeyboardButton(text="get category info", callback_data="m_get")
m_status = InlineKeyboardButton(text="status", callback_data="m_status")
u_main_keyboard = InlineKeyboardMarkup()
u_main_keyboard.row(m_init,m_get)
u_main_keyboard.row(m_status)




bot_perivious_msg = ""
#start command...
@bot.message_handler(commands=['23785JuniorMedia'])
def Admin_Recognize(message):
        global bot_perivious_msg
        bot.send_message(message.chat.id ,"Hello <b>Mohammad Ali!</b> 😄 Welcome to your bot , <i>JuniorMedia</i>!...Choose a commannd ⤵️ to START...",reply_markup=u_main_keyboard , parse_mode="HTML")
        bot_perivious_msg = message.message_id + 1








current_category = ""
current_commit = ""

#callback handler
@bot.callback_query_handler(func= lambda call:True)
def callback_handler(call):
        global current_category
        global current_commit
        global bot_perivious_msg
        if call.data == "m_init" :
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id , "OK!...Now, Enter your category_name: ")
                bot.register_next_step_handler(call.message,get_user_category)
                bot_perivious_msg = call.message.message_id + 1
        elif call.data == "m_status" :
                categories_list =[]
                str = f"""
                    current category : ➡️ {current_category}
   All categories :
"""
                
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                with sqlite3.connect('master.db') as connection:
                    cursor = connection.cursor()
                    Get_Current_categories = """
                    SELECT * FROM categories
                    """
                    cursor.execute(Get_Current_categories)
                    categories_list = cursor.fetchall()
                c = 0
                for c_info in categories_list:
                     c = c + 1
                     str+=f"""     id){c_info[0]} name)⏩<b>{c_info[1]}</b> messages)<b>{c_info[2]}</b>
"""
                
                str += f"total categories : {c} ✅"
                bot.send_message(call.message.chat.id , str, parse_mode="HTML")
                bot_perivious_msg = bot_perivious_msg + 1
        elif call.data == "m_get" :
                categories_list =[]
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                with sqlite3.connect('master.db') as connection:
                    cursor = connection.cursor()
                    Get_Current_categories = """
                    SELECT * FROM categories
                    """
                    cursor.execute(Get_Current_categories)
                    categories_list = cursor.fetchall()
                categories_keyboard = InlineKeyboardMarkup()
                for category in categories_list:
                       c_get = InlineKeyboardButton(text=f"{category[1]} 📊 {category[2]}", callback_data=f"{category[1]}")
                       categories_keyboard.row(c_get)
                E_S = InlineKeyboardButton(text=f"External search for? 🔎", callback_data="E_s")
                categories_keyboard.row(E_S)
                bot.send_message(call.message.chat.id,f"You have your all categories her:",reply_markup=categories_keyboard)
                bot_perivious_msg = bot_perivious_msg + 1
        elif call.data == "c_add":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id , "Enter a title :")
                bot.register_next_step_handler(call.message,get_user_category_title)
                bot_perivious_msg = call.message.message_id + 1
        elif call.data == "c_search":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id,f"enter a Keyword to search for on commits into <i>{current_category}</i>", parse_mode="HTML")
                bot.register_next_step_handler(call.message,searchforcurrentcategory)

                bot_perivious_msg = bot_perivious_msg + 1
        elif call.data == "E_s":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id,f"Enter a Keyword to search for on all commits")
                bot.register_next_step_handler(call.message,externalsearchfor)

                bot_perivious_msg = bot_perivious_msg + 1
        elif call.data == "c_delete":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id,f"✅❌Are you sure you are realy going to delete <u>{current_category}</u> from memory? your sent messages dose not delete bot their addreses will be terminated! YES/NO ", parse_mode="HTML")
                bot.register_next_step_handler(call.message,deletCat)
        elif  "commit_delet" in call.data.strip():
                
                current_commit=call.data[12:]
                print(call.data)
                bot.send_message(call.message.chat.id,f"✅❌Are you sure you are realy going to delete <u>{current_commit}</u> from memory? your sent messages dose not delete bot their addreses will be terminated! YES/NO ", parse_mode="HTML")
                bot.register_next_step_handler(call.message,deletComm)
        elif  "commit_update" in call.data.strip():
                
                current_commit=call.data[13:]
                print(call.data)
                bot.send_message(call.message.chat.id,f"Enter your new title for <b>{current_commit}</b> to change:",parse_mode="HTML")
                bot.register_next_step_handler(call.message,updateComm)

                
        elif call.data == "c_update":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id,f"Enter new title for <i>{current_category}</i>",parse_mode="HTML")
                bot.register_next_step_handler(call.message,updatecat)

                bot_perivious_msg = bot_perivious_msg + 1

        elif call.data == "c_see":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                messages_list = []
                bool = False
                #global current_category
                with sqlite3.connect('master.db') as connection:
                    cursor = connection.cursor()
                    Get_Current_categories_messages = """
                    SELECT * FROM message_ids 
                    """
                    cursor.execute(Get_Current_categories_messages)
                    messages_list = cursor.fetchall()
                for msg in messages_list:
                    if msg[3] == current_category:
                        bool = True
                        commit_delete = InlineKeyboardButton(text=f"❌Delete {msg[2]}", callback_data=f"commit_delet{msg[2]}", parse_mode="HTML")
                        commit_update = InlineKeyboardButton(text=f"📳Update {msg[2]}", callback_data=f"commit_update{msg[2]}", parse_mode="HTML")
                        commit_keyboard =  InlineKeyboardMarkup()
                        commit_keyboard.row(commit_delete,commit_update)
                        bot.send_message(call.message.chat.id , f"{msg[2]}",  reply_to_message_id=msg[1] , reply_markup=commit_keyboard)
                if bool == False:
                       bot.send_message(call.message.chat.id , f"❌There is no saved message for <u>{current_category}</u> yet! you can send a message with send content...❌",parse_mode="HTML")
                       
                    
        else:
               
               current_category = call.data
               bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
               c_add = InlineKeyboardButton(text="send content ✉️", callback_data="c_add")
               c_see = InlineKeyboardButton(text="see contents 😶", callback_data="c_see")
               c_search = InlineKeyboardButton(text="search for? 🔎", callback_data="c_search")
               c_delete = InlineKeyboardButton(text=f"Delete {current_category} ❌", callback_data="c_delete")
               c_update = InlineKeyboardButton(text=f"Update {current_category} title 📳", callback_data="c_update")
               c_addorsee_keboard = InlineKeyboardMarkup()
               c_addorsee_keboard.row(c_add,c_see)
               c_addorsee_keboard.row(c_search)
               c_addorsee_keboard.row(c_update)
               c_addorsee_keboard.row(c_delete)
               bot.send_message(call.message.chat.id , f"How do you wanna handle the category <u>{current_category}</u>?",reply_markup=c_addorsee_keboard, parse_mode="HTML")
               bot_perivious_msg = call.message.message_id + 1

                

               
                       





#register_next_step_handlers
def get_user_category(message):
        global bot_perivious_msg
        bot.delete_message(chat_id= message.chat.id,message_id=bot_perivious_msg)
        c_name = message.text
        with sqlite3.connect('master.db') as connection:
            cursor = connection.cursor()
            Create_NEW_category = """
            INSERT INTO categories (c_name,c_counter)
            VALUES (?,?)
            """
            category_register_tuple = (c_name ,0)
            cursor.execute(Create_NEW_category,category_register_tuple)
        bot.reply_to(message,f"🥳🥳🥳New category <b>{c_name}</b> has been initialized succesfully!🥳🥳🥳", parse_mode="HTML")
        bot_perivious_msg = message.message_id + 1

title = ""
def get_user_category_title(message):
       global title
       global bot_perivious_msg
       title = message.text
       bot.delete_message(chat_id= message.chat.id,message_id=bot_perivious_msg)
       bot.reply_to(message,f"Title : <u>{title}</u> ; Now send me your message for category : <b>{current_category}</b> ...", parse_mode="HTML")
       bot.register_next_step_handler(message,get_user_category_message)
       bot_perivious_msg = message.message_id + 1

category_list = []
current_category_counter = 0
def get_user_category_message(message):
       msg_id = message.message_id
       global bot_perivious_msg
       global category_list
       global current_category_counter
       with sqlite3.connect('master.db') as connection:
            cursor = connection.cursor()
            Add_NEW_Content = """
            INSERT INTO message_ids (message_ids,message_title,message_subcategory_name)
            VALUES (?,?,?)
            """
            content_register_tuple = (msg_id , title , current_category)
            cursor.execute(Add_NEW_Content,content_register_tuple)
            
            Get_Current_categories_counter = """
            SELECT * FROM categories 
            """
            cursor.execute(Get_Current_categories_counter)
            category_list = cursor.fetchall()
            for ctg in category_list:
                if ctg[1] == current_category:
                      current_category_counter = ctg[2]
                      
            cursor.execute("""
                  UPDATE categories
                   SET c_counter = ?
                   WHERE c_name = ?;
                   """, (current_category_counter + 1, current_category))
       bot.delete_message(chat_id= message.chat.id,message_id=bot_perivious_msg)
       bot.reply_to(message,f"This message has been saved succesfully for next searchs!🥳🥳🥳")
       bot_perivious_msg = message.message_id + 1

def searchforcurrentcategory(message):
        s_key = message.text
        co = 0
        with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                Get_Current_categories_messages = """
                SELECT * FROM message_ids 
                """
                cursor.execute(Get_Current_categories_messages)
                messages_list = cursor.fetchall()
        for msg in messages_list:
                if msg[3] == current_category and s_key in msg[2]:
                        co += 1
                        bot.send_message(message.chat.id , f"{msg[2]}",  reply_to_message_id=msg[1])

        if co > 0:
               bot.send_message(message.chat.id , f"✅<b>{co}</b> commits founded with key: <u>{s_key}</u>.✅", parse_mode="HTML")
        else:
               bot.send_message(message.chat.id , f"❌NO commits founded with key: <b>{s_key}</b>!!!❌", parse_mode="HTML")
def externalsearchfor(message):
        s_key = message.text
        co = 0
        with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                Get_Current_categories_messages = """
                SELECT * FROM message_ids 
                """
                cursor.execute(Get_Current_categories_messages)
                messages_list = cursor.fetchall()
        for msg in messages_list:
                if s_key in msg[2]:
                        co += 1
                        bot.send_message(message.chat.id , f"{msg[2]}",  reply_to_message_id=msg[1])

        if co > 0:
               bot.send_message(message.chat.id , f"✅<b>{co}</b> commits founded with key: <b>{s_key}</b>.✅", parse_mode="HTML")
        else:
               bot.send_message(message.chat.id , f"❌NO commits founded with key: <b>{s_key}</b>!!!❌", parse_mode="HTML")

def deletCat(message):
       if message.text == "NO":
              bot.send_message(message.chat.id , f"🤚🤚🤚Termination <i>{current_category}</i> canceled!🤚🤚🤚", parse_mode="HTML")
       elif message.text == "YES":
              with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM message_ids WHERE message_subcategory_name = ?", (current_category,))
                cursor.execute("DELETE FROM categories WHERE c_name  = ?", (current_category,))
              bot.reply_to(message,f"The category {current_category} has been deleted succesfully!✅")
       else:
           bot.reply_to(message,f"🚫🚫🚫<tg-spoiler>{message.text}</tg-spoiler> is unknown command!!!!🚫🚫🚫", parse_mode="HTML")   
def deletComm(message):
       if message.text == "NO":
              bot.send_message(message.chat.id , f"🤚🤚🤚Termination <b>{current_commit}</b> canceled!🤚🤚🤚", parse_mode="HTML")
       elif message.text == "YES":
              with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM message_ids WHERE message_title = ?", (current_commit,))

                
                Get_Current_categories_counter = """
                         SELECT * FROM categories 
                        """
                cursor.execute(Get_Current_categories_counter)
                category_list = cursor.fetchall()
                for ctg in category_list:
                        if ctg[1] == current_category:
                                current_category_counter = ctg[2]
                      
                cursor.execute("""
                  UPDATE categories
                   SET c_counter = ?
                   WHERE c_name = ?;
                   """, (current_category_counter - 1, current_category))

              bot.reply_to(message,f"The commit <s>{current_commit}</s> has been deleted succesfully!✅", parse_mode="HTML")
       else:
           bot.reply_to(message,f"🚫🚫🚫<tg-spoiler>{message.text}</tg-spoiler> is unknown command!!!!🚫🚫🚫", parse_mode="HTML")   

def updatecat(message):
       with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""
                  UPDATE categories
                   SET c_name = ?
                   WHERE c_name = ?;
                   """, (message.text, current_category))
       bot.reply_to(message,f"✏️✏️✏️<s>{current_category}</s> changed into <b>{message.text}</b> succesfully!✏️✏️✏️", parse_mode="HTML")  
def updateComm(message):
       with sqlite3.connect('master.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""
                  UPDATE message_ids
                   SET message_title = ?
                   WHERE message_title = ?;
                   """, (message.text, current_commit))
       bot.reply_to(message,f"✏️✏️✏️<s>{current_commit}</s> changed into <b>{message.text}</b> succesfully!✏️✏️✏️", parse_mode="HTML")  
       
              



       

bot.polling()