# -*- coding: utf-8 -*-
import telebot 
from telebot import types,util 
import sys 
import redis as REDIS 
import random
import string
import os
import requests
import re
import json
reload(sys) 
sys.setdefaultencoding("utf-8") 
redis = REDIS.StrictRedis(host='localhost', port=6379, db=3)
bot = telebot.TeleBot('348188814:AAEJGyZvUNwB2G39BDxu61eRUfZhGzXdvYM')
print("\nBot Has Been Launched")
# Define's
admins = [65761134,113566842,133021344,0000]
send = bot.send_message
BOT = bot.get_me().id
BOTu = bot.get_me().username

#####################
@bot.message_handler(content_types=['text','photo','video','documnet'])
def Texts(msg) :
	if msg.text :
		if msg.text == "/start":
			if msg.chat.type == "private" :
				if redis.sismember("T3_Bot_Stats:Users",msg.from_user.id) != True:
					redis.sadd("T3_Bot_Stats:Users",msg.from_user.id)
			if redis.sismember("T3_Bot_Stats:All",msg.chat.id) != True:
				redis.sadd("T3_Bot_Stats:All",msg.chat.id)
			Text = (redis.hget("T3_Bot","WelCome_Message") or "Hi")
			send(msg.chat.id,Text)

		if msg.chat.id in admins :
			if msg.text == "/panel" :
				Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
				Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
				Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
				send(msg.chat.id,"پنل مدیریت : ",reply_markup=Button)
			if msg.text == "آمار" :
				Users = int(redis.scard("T3_Bot_Stats:Users"))
				Groups = int(redis.scard("T3_Bot_Stats:Groups"))
				All = int(redis.scard("T3_Bot_Stats:All"))
				send(msg.chat.id,"آمار دقیق ربات تا این لحظه :\n\nکاربران: {}\nگروه ها: {}\nهمه : {}\n\n{}".format(Users,Groups,All,BOTu))
			if msg.text == "پیغام همگانی" :
				Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
				Button.add(types.KeyboardButton("بنر جدید"),types.KeyboardButton("بنر آماده"))
				Button.add(types.KeyboardButton("بازگشت"))
				z = send(msg.chat.id,"انتخاب کنید : ",reply_markup=Button)
				bot.register_next_step_handler(z, BroadCast)
			if msg.text == "متن خوش آمد گویی" :
				WelCome = (redis.hget("T3_Bot","WelCome_Message") or "`تنظیم نشده`")
				Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
				Button.add(types.KeyboardButton("تعویض متن"),types.KeyboardButton("بازگشت"))
				z = send(msg.chat.id,"متن فعلی خوش آمدگویی : \n----------------\n{}\n----------------\nبرای تعویض متن از دکمه زیر استفاده نمایید".format(WelCome),parse_mode="markdown",reply_markup=Button)
				bot.register_next_step_handler(z, Set_Welcome)			
			if msg.text == "/fwdall" :
				q = msg.reply_to_message.message_id
				for i in redis.smembers("T3_Bot_Stats:All") :
					try:
						bot.forward_message(i,msg.chat.id,q)
					except:
						pass
				Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
				Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
				Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))			
				send(msg.chat.id,"ارسال شد!",reply_markup=Button)
			if msg.text == "بازگشت" :
				Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
				Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
				Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
				send(msg.chat.id,"منوی اصلی :",reply_markup=Button)
			if msg.reply_to_message:
				q = msg.reply_to_message.message_id
# Set Welcome Steps
def Set_Welcome(msg):
	if msg.text == "تعویض متن":
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("بازگشت"))
		z = send(msg.chat.id,"متن جدید را ارسال کنید : ",reply_markup=Button)
		bot.register_next_step_handler(z, Set_Welcome_Text)
def Set_Welcome_Text(msg) :
	if msg.text != "بازگشت" :
		redis.hset("T3_Bot","WelCome_Message",msg.text) 
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
		Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
		send(msg.chat.id,"متن جدید خوش آمدگویی تنظیم شد!",reply_markup=Button)		
# Set NewGp Steps		
def Set_New_GP(msg):
	if msg.text == "تعویض متن":
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("بازگشت"))
		z = send(msg.chat.id,"متن جدید را ارسال کنید : ",reply_markup=Button)
		bot.register_next_step_handler(z, Set_New_GP_Text)
def Set_New_GP_Text(msg) :
	if msg.text != "بازگشت" :
		redis.hset("T3_Bot","New_Gp_Message",msg.text) 
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
		Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
		send(msg.chat.id,"متن جدید گروه جدید تنظیم شد!",reply_markup=Button)				
		
def BroadCast(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "بنر آماده" :
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("بازگشت"))
			z = send(msg.chat.id,"بنر را ارسال کنید : \n\n",reply_markup=Button)
			bot.register_next_step_handler(z, BroadCast_s2)	
		if msg.text == "بنر جدید" :
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("بازگشت"))
			z = send(msg.chat.id,"بنر را ارسال کنید : \n\n",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner)
def BroadCast_s2(msg) :
	if msg.text != "بازگشت" :
		for i in redis.smembers("T3_Bot_Stats:All") :
			try:
				send(i,msg.text)
			except:
				pass
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
		Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
		send(msg.chat.id,"ارسال شد!",reply_markup=Button)
def Create_Banner(msg) :
	if msg.text :
		redis.hset('T3_Bot:Create_Banner',"Type","Text")
		redis.hset('T3_Bot:Create_Banner',"TEXT",msg.text)
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("زیرنویس نمیخواهم"),types.KeyboardButton("بازگشت"))
		z = send(msg.from_user.id,"زیرنویس را ارسال کنید :\n\nنکته : اگر زیرنویس نمیخواهید دکمه 'زیرنویس نمیخواهم' را ارسال کنید",reply_markup=Button)
		bot.register_next_step_handler(z, Create_Banner_Text_s2)
	elif msg.photo :
		redis.hset('T3_Bot:Create_Banner',"Type","Photo")
		redis.hset('T3_Bot:Create_Banner',"File_ID",msg.photo[2].file_id)
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("زیرنویس نمیخواهم"),types.KeyboardButton("بازگشت"))
		z = send(msg.from_user.id,"زیرنویس را ارسال کنید :\n\nنکته : اگر زیرنویس نمیخواهید دکمه 'زیرنویس نمیخواهم' را ارسال کنید",reply_markup=Button)
		bot.register_next_step_handler(z, Create_Banner_Photo_s2)
	elif msg.video :
		redis.hset('T3_Bot:Create_Banner',"Type","Video")
		redis.hset('T3_Bot:Create_Banner',"File_ID",msg.video.file_id)
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("زیرنویس نمیخواهم"),types.KeyboardButton("بازگشت"))
		z = send(msg.from_user.id,"زیرنویس را ارسال کنید :\n\nنکته : اگر زیرنویس نمیخواهید دکمه 'زیرنویس نمیخواهم' را ارسال کنید",reply_markup=Button)
		bot.register_next_step_handler(z, Create_Banner_Video_s2)
	elif msg.documnet :
		redis.hset('T3_Bot:Create_Banner',"Type","Doc")
		redis.hset('T3_Bot:Create_Banner',"File_ID",msg.documnet.file_id)
		Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
		Button.add(types.KeyboardButton("زیرنویس نمیخواهم"),types.KeyboardButton("بازگشت"))
		z = send(msg.from_user.id,"زیرنویس را ارسال کنید :\n\nنکته : اگر زیرنویس نمیخواهید دکمه 'زیرنویس نمیخواهم' را ارسال کنید",reply_markup=Button)
		bot.register_next_step_handler(z, Create_Banner_Documnet_s2)


def Create_Banner_Text_s2(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون دکمه" :
			q = redis.hget('T3_Bot:Create_Banner',"TEXT")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					send(i,q)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			q = redis.hget('T3_Bot:Create_Banner',"TEXT")
			for i in msg.text.split('\n') :		
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					send(i,q,reply_markup=markup)
				except:
					pass	
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
				

def Create_Banner_Photo_s2(msg):
	if msg.text != "بازگشت" :
		if msg.text == "زیرنویس نمیخواهم" :
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Photo_s3_noc)	
		else:
			redis.hset('T3_Bot:Create_Banner',"Caption",msg.text)
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Photo_s3)	
def Create_Banner_Photo_s3(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون کیبورد" :
			c = redis.hget('T3_Bot:Create_Banner',"Caption")
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_photo(i,q,caption=c)
				except:
					pass	
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			q = redis.hget('T3_Bot:Create_Banner',"Caption")
			for i in msg.text.split('\n') :	
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_photo(i,ph,caption=q,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
def Create_Banner_Photo_s3_noc(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون کیبورد" :
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_photo(i,q)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in msg.text.split('\n') :
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_photo(i,ph,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
def Create_Banner_Video_s2(msg):
	if msg.text != "بازگشت" :
		if msg.text == "زیرنویس نمیخواهم" :
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Video_s3_noc)	
		else:
			redis.hset('T3_Bot:Create_Banner',"Caption",msg.text)
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Video_s3)	
def Create_Banner_Video_s3(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون کیبورد" :
			c = redis.hget('T3_Bot:Create_Banner',"Caption")
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_video(i,q,caption=c)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			q = redis.hget('T3_Bot:Create_Banner',"Caption")
			for i in msg.text.split('\n') :	
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_video(i,ph,caption=q,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
def Create_Banner_Video_s3_noc(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون کیبورد" :
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_video(i,q)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in msg.text.split('\n') :	
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_video(i,ph,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)

	
def Create_Banner_Documnet_s2(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "زیرنویس نمیخواهم" :
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Doc_s3_noc)	
		else:
			redis.hset('T3_Bot:Create_Banner',"Caption",msg.text)
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("ارسال بدون کیبورد"),types.KeyboardButton("بازگشت"))
			z = send(msg.from_user.id,"کیبورد اینلاین را ارسال کنید :\n\nنکته : اگر کیبورد ندارید دکمه 'ارسال بدون کیبورد' را ارسال کنید",reply_markup=Button)
			bot.register_next_step_handler(z, Create_Banner_Doc_s3)	
def Create_Banner_Doc_s3(msg) :
	if msg.text != "بازگشت" :
		if msg.text == "ارسال بدون کیبورد" :
			c = redis.hget('T3_Bot:Create_Banner',"Caption")
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_documnet(i,q,caption=c)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			q = redis.hget('T3_Bot:Create_Banner',"Caption")
			for i in msg.text.split('\n') :		
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_documnet(i,ph,caption=q,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
def Create_Banner_Doc_s3_noc(msg) :
	if msg.text != "بازگشت" :

		if msg.text == "ارسال بدون کیبورد" :
			q = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_documnet(i,q)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
		else:
			markup = types.InlineKeyboardMarkup()
			ph = redis.hget('T3_Bot:Create_Banner',"File_ID")
			for i in msg.text.split('\n') :		
				try:
					markup.add(types.InlineKeyboardButton(i.split("|")[0],url=i.split("|")[1]))
				except:
					pass
			for i in redis.smembers("T3_Bot_Stats:All") :
				try:
					bot.send_documnet(i,ph,reply_markup=markup)
				except:
					pass
			Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
			Button.add(types.KeyboardButton("آمار"),types.KeyboardButton("پیغام همگانی"))
			Button.add(types.KeyboardButton("متن خوش آمد گویی"),types.KeyboardButton("متن گروه جدید"))
			send(msg.chat.id,"ارسال شد!",reply_markup=Button)
			
	
@bot.message_handler(content_types=['new_chat_member'])
def Add(msg) :		
	if str(msg.new_chat_member.id) == str(BOT):
		redis.sadd("T3_Bot_Stats:Groups",msg.chat.id)
		redis.sadd("T3_Bot_Stats:All",msg.chat.id)
@bot.message_handler(content_types=['left_chat_member'])
def Left(msg) :		
	if str(msg.left_chat_member.id) == str(BOT):
		redis.srem("T3_Bot_Stats:Groups",msg.chat.id)
		redis.srem("T3_Bot_Stats:All",msg.chat.id)

bot.polling(True)
		
		
