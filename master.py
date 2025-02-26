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
u_main_keyboard = InlineKeyboardMarkup()
u_main_keyboard.row(m_init,m_get)



#start command...
@bot.message_handler(commands=['23785JuniorMedia'])
def Admin_Recognize(message):
        bot.send_message(message.chat.id ,"Hellow Mohammad Ali! Welcome to your bot , JuniorMedia!...Choose a commannd to START...",reply_markup=u_main_keyboard)








current_category = ""
#callback handler
@bot.callback_query_handler(func= lambda call:True)
def callback_handler(call):
        if call.data == "m_init" :
                bot.send_message(call.message.chat.id , "OK!...Now, Enter your category_name: ")
                bot.register_next_step_handler(call.message,get_user_category)
        elif call.data == "m_get" :
                categories_list =[]
                with sqlite3.connect('master.db') as connection:
                    cursor = connection.cursor()
                    Get_Current_categories = """
                    SELECT * FROM categories
                    """
                    cursor.execute(Get_Current_categories)
                    categories_list = cursor.fetchall()
                categories_keyboard = InlineKeyboardMarkup()
                for category in categories_list:
                       c_get = InlineKeyboardButton(text=f"{category[1]}", callback_data=f"{category[1]}")
                       categories_keyboard.row(c_get)
                bot.reply_to(call.message,f"Your have your all categories her:",reply_markup=categories_keyboard)
        elif call.data == "c_add":
                bot.send_message(call.message.chat.id , "Enter a title :")
                bot.register_next_step_handler(call.message,get_user_category_title)
        elif call.data == "c_see":
                
                messages_list = []
                global current_category
                with sqlite3.connect('master.db') as connection:
                    cursor = connection.cursor()
                    Get_Current_categories_messages = """
                    SELECT * FROM message_ids 
                    """
                    cursor.execute(Get_Current_categories_messages)
                    messages_list = cursor.fetchall()
                for msg in messages_list:
                    if msg[3] == current_category:
                        message_link = f"https://t.me/Junior_mediaBOT/{msg[1]}"
                        bot.send_message(call.message.chat.id , f"{msg[2]}",  reply_to_message_id=msg[1])
                    
        else:
               
               current_category = call.data
               
               c_add = InlineKeyboardButton(text="send content", callback_data="c_add")
               c_see = InlineKeyboardButton(text="see contents", callback_data="c_see")
               c_addorsee_keboard = InlineKeyboardMarkup()
               c_addorsee_keboard.row(c_add,c_see)
               bot.send_message(call.message.chat.id , f"Hw do you wanna handle the category {current_category}?",reply_markup=c_addorsee_keboard)
               

                

               
                       





#register_next_step_handlers
def get_user_category(message):
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

title = ""
def get_user_category_title(message):
       global title
       title = message.text
       bot.reply_to(message,f"title : {title} ; Now send me your message for category : {current_category} ...")
       bot.register_next_step_handler(message,get_user_category_message)


def get_user_category_message(message):
       msg_id = message.message_id
       with sqlite3.connect('master.db') as connection:
            cursor = connection.cursor()
            Add_NEW_Content = """
            INSERT INTO message_ids (message_ids,message_title,message_subcategory_name)
            VALUES (?,?,?)
            """
            content_register_tuple = (msg_id , title , current_category)
            cursor.execute(Add_NEW_Content,content_register_tuple)
       bot.reply_to(message,f"This message has been saved succesfully for next searchs!")




       

bot.polling()