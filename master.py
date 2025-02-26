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





bot.polling()