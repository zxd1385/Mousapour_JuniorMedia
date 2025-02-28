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
        bot.send_message(message.chat.id ,"Hellow Mohammad Ali! Welcome to your bot , JuniorMedia!...Choose a commannd to START...",reply_markup=u_main_keyboard)
        bot_perivious_msg = message.message_id + 1








current_category = ""

#callback handler
@bot.callback_query_handler(func= lambda call:True)
def callback_handler(call):
        global current_category
        global bot_perivious_msg
        if call.data == "m_init" :
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id , "OK!...Now, Enter your category_name: ")
                bot.register_next_step_handler(call.message,get_user_category)
                bot_perivious_msg = call.message.message_id + 1
        elif call.data == "m_status" :
                categories_list =[]
                str = f"""
                    current category : {current_category}
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
                     str+=f"""     id){c_info[0]} name){c_info[1]} messages){c_info[2]}
"""
                
                str += f"total categories : {c}"
                bot.send_message(call.message.chat.id , str)
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
                       c_get = InlineKeyboardButton(text=f"{category[1]} 🔑{category[2]}", callback_data=f"{category[1]}")
                       categories_keyboard.row(c_get)
                bot.send_message(call.message.chat.id,f"Your have your all categories her:",reply_markup=categories_keyboard)
                bot_perivious_msg = bot_perivious_msg + 1
        elif call.data == "c_add":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id , "Enter a title :")
                bot.register_next_step_handler(call.message,get_user_category_title)
                bot_perivious_msg = call.message.message_id + 1
        elif call.data == "c_search":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                bot.send_message(call.message.chat.id,f"enter a Keyword to search for on commits into {current_category}")
                bot.register_next_step_handler(call.message,searchforcurrentcategory)

                bot_perivious_msg = bot_perivious_msg + 1

        elif call.data == "c_see":
                bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
                messages_list = []
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
                        bot.send_message(call.message.chat.id , f"{msg[2]}",  reply_to_message_id=msg[1])
                    
        else:
               
               current_category = call.data
               bot.delete_message(chat_id= call.message.chat.id,message_id=bot_perivious_msg)
               c_add = InlineKeyboardButton(text="send content", callback_data="c_add")
               c_see = InlineKeyboardButton(text="see contents", callback_data="c_see")
               c_search = InlineKeyboardButton(text="search for?", callback_data="c_search")
               c_addorsee_keboard = InlineKeyboardMarkup()
               c_addorsee_keboard.row(c_add,c_see)
               c_addorsee_keboard.row(c_search)
               bot.send_message(call.message.chat.id , f"Hw do you wanna handle the category {current_category}?",reply_markup=c_addorsee_keboard)
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
        bot.reply_to(message,f"New category {c_name} has been initialized succesfully1")
        bot_perivious_msg = message.message_id + 1

title = ""
def get_user_category_title(message):
       global title
       global bot_perivious_msg
       title = message.text
       bot.delete_message(chat_id= message.chat.id,message_id=bot_perivious_msg)
       bot.reply_to(message,f"title : {title} ; Now send me your message for category : {current_category} ...")
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
       bot.reply_to(message,f"This message has been saved succesfully for next searchs!")
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
               bot.send_message(message.chat.id , f"{co} commits founded with key: {s_key}.")
        else:
               bot.send_message(message.chat.id , f"NO commits founded with key: {s_key}!!!")



       

bot.polling()