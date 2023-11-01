import os
import re

import telebot
import wikipedia
from zhconv import zhconv

API_TOKEN = os.environ.get("API_TOKEN")

LANGUAGE = 'zh'


class WikiBot:
    def __init__(self):
        self.wiki = wikipedia


def wikiparse(page):
    if LANGUAGE.__eq__('en'):
        str = '.'
    else:
        str = '。'
    wikitext = page.content[:4000]
    wikimas = wikitext.split(str)
    wikimas = wikimas[:-1]
    wikitext2 = ''
    for x in wikimas:
        if not ('==' in x):
            if len((x.strip())) > 6:
                wikitext2 = wikitext2 + x + str
        else:
            break
    # Now, using regular expressions, we remove the markup
    wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
    wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
    wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
    new_str = zhconv.convert(wikitext2, 'zh-hans')
    return new_str


def getwiki(wiki, text):
    try:
        if LANGUAGE.__eq__('en'):
            str = 'en'
        else:
            str = 'zh'
        direct_search = wiki.page(text, auto_suggest=False)
        msg = wikiparse(direct_search)
        info = '更多信息请访问: ' + 'https://' + str + '.wikipedia.org/wiki/' + text
        return msg + '\n\n' + info
    # Handling an exception that the wikipedia module could return
    except wikipedia.exceptions.DisambiguationError as e:
        opt = e.options
        msg = "对不起，您的查询太模糊了！\n" \
              "'{0}' 可能指的是:\n" \
              "\n<b>{1}</b>\n" \
              "\n尝试搜索上述的其中一个建议。".format(e.title, opt)
        return msg
    except wikipedia.exceptions.PageError:
        return '对不起，我找不到关于这个主题的任何信息，可能该词条还没有建立。😔'


if __name__ == "__main__":
    bot = telebot.TeleBot(token=API_TOKEN)
    current_chats = {}


    @bot.message_handler(commands=['start'])
    def welcome(message):
        chat_id = message.chat.id

        wb = WikiBot()
        current_chats[chat_id] = wb
        current_chats[chat_id].wiki.set_lang("zh")  # 默认语言

        bot.send_message(chat_id,
                         "你好, {0.first_name}!\n"
                         "我的名字是Telegram Wikipedias Bot，我是一个让你在这里直接搜索维基百科文章的机器人。 \n"
                         "把我当作你的个人维基百科搜索工具😉\n"
                         "\n输入任何单词，让我们开始学习吧！"""
                         "\n\n<b>可使用命令:</b>"
                         "\n/start - 开始使用bot"
                         "\n/help - 显示帮助信息"
                         "\n/chinese - 设置为中文搜索结果 (默认)"
                         "\n/eng - 设置为英文搜索结果".format(message.from_user, bot.get_me()),
                         parse_mode='html')


    @bot.message_handler(commands=['help'])
    def command_help(message):
        chat_id = message.chat.id  # Getting id of the chat
        bot.send_message(chat_id, "\n\n<b>可用命令:</b>"
                                  "\n/start - 开始使用bot"
                                  "\n/help - 显示帮助信息"
                                  "\n/chinese - 设置为中文搜索结果 (默认)"
                                  "\n/eng - 设置为英文搜索结果",
                         parse_mode='html')


    @bot.message_handler(commands=['chinese'])
    def change_lang_ru(message):
        chat_id = message.chat.id  # Getting id of the chat
        if chat_id not in current_chats.keys():
            bot.send_message(chat_id, "请先运行该命令 /start")
        else:
            global LANGUAGE
            LANGUAGE = 'zh'
            current_chats[chat_id].wiki.set_lang("zh")
            bot.send_message(chat_id, "设置为中文搜索结果")


    @bot.message_handler(commands=['eng'])
    def change_lang_ru(message):
        chat_id = message.chat.id  # Getting id of the chat
        if chat_id not in current_chats.keys():
            bot.send_message(chat_id, "请使用 /start 命令使用")
        else:
            global LANGUAGE
            LANGUAGE = 'en'
            current_chats[chat_id].wiki.set_lang("en")
            bot.send_message(chat_id, "设置为英文搜索结果")


    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        chat_id = message.chat.id  # Getting id of the chat
        if chat_id not in current_chats.keys():
            bot.send_message(chat_id, "请使用 /start 命令使用")
        else:
            msg = getwiki(current_chats[chat_id].wiki, message.text)
            bot.send_message(chat_id, msg, parse_mode='html')


    # Start
    bot.polling(none_stop=True)
