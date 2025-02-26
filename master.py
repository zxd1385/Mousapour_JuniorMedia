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
        message_subcategory_name integer
         );
        """
        cursor.execute(Create_Table_categories)


#main_keyword
m_init = InlineKeyboardButton(text="initialize new category", callback_data="m_init")
m_get = InlineKeyboardButton(text="get category info", callback_data="m_get")
u_main_keyboard = InlineKeyboardMarkup()
u_main_keyboard.row(m_init,m_get)



#start command...
@bot.message_handler(commands=['23785JuniorMedia'])
def Admin_Recognize(message):
        bot.send_message(message.chat.id ,"Hellow Mohammad Ali! Welcome to your bot , JuniorMedia!...Choose a commannd to START...",reply_markup=u_main_keyboard)








#callback handler
@bot.callback_query_handler(func= lambda call:True)
def callback_handler(call):
        if call.data == "m_init" :
                bot.send_message(call.message.chat.id , "OK!...Now, Enter your category_name: ")
                bot.register_next_step_handler(call.message,get_user_category)





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

bot.polling()