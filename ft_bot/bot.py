# -*- coding: utf-8 -*-
import time
import vk_api
import random
import re
import os
import json
import smtplib
import apiai 
import wikipedia
from googletrans import Translator
from email.mime.text import MIMEText
from email.header import Header
from vk_api.longpoll import VkLongPoll, VkEventType

# ranepa.fintech@gmail.com fintechranepa


neir='Высокоуровневый ИИ для принятия решений'

kbr= { 
    "one_time": False, 
    "buttons": [ 
        [
          { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"5\"}", 
          "label": "МЕНЮ" 
        }, 
        "color": "primary" 
      }
      ],
      [{ 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"1\"}", 
          "label": 'Расписание'
        }, 
        "color": "positive" 
      }
      , 
      { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"3\"}", 
          "label": "Заказать справку" 
        }, 
        "color": "positive" 
      }
      ], 
      [{ 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"3\"}", 
          "label": "Контакты" 
        }, 
        "color": "default" 
      }, 
     { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"4\"}", 
          "label": "Тут что-то еще" 
        }, 
        "color": "default" 
      }, 
     { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"5\"}", 
          "label": "И тут" 
        }, 
        "color": "default" 
      }
      ] ,[
          { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"4\"}", 
          "label": "Написать в деканат (анонимно)" 
        }, 
        "color": "default" 
      }
      ],[
          { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"4\"}", 
          "label": "Дополнительно" 
        }, 
        "color": "default" 
      }
      ]
    ] 
  } 

kbr2= { 
    "one_time": False, 
    "buttons": [ 
      [{ 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"1\"}", 
          "label": 'Как я работаю?'
        }, 
        "color": "positive" 
      },
          { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"2\"}", 
          "label": 'Перевести'
        }, 
        "color": "positive" 
      }
      ],[ 
    { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"2\"}", 
          "label": neir
        }, 
        "color": "positive" 
      }
      ],
    [ 
      { 
        "action": { 
          "type": "text", 
          "payload": "{\"button\": \"3\"}", 
          "label": "<<<<Назад" 
        }, 
        "color": "negative" 
      }
      ]
    ] 
  } 

#Здесь нужно вставить настоящий токен
token = vk_api.VkApi(token='asdvfsafgdfsdgsdafsdaewadfsgddafsgdsdafsgdsdafsgsdafsgdsdasgdas')

# Текст помощи
hlp=' \n\n______&#128203;МЕНЮ&#128203;_____ \n 1&#8419; - расписание\n 2&#8419; - заказать справку\n 3&#8419; - карты корпусов\n 4&#8419; - контакты\n Чтобы увидеть дополнительные функции напиши слово "еще"'
hlp2='\n 5&#8419; - как я работаю\n 6&#8419; - википедия\n 7&#8419; - переводчик\n 8&#8419; - бросить монетку'
contacts='\nМАРГАРИТА АЛЬБЕРТОВНА КАЗАРЯН  \n-Руководитель ОНЭ  \n-Зам. декана Экономического факультета  \n-Доктор экономических наук, доцент  \n&#9742; (495) 937-07-44  \n&#128233; km@ranepa.ru  \n\n ИРИНА НИКОЛАЕВНА МЕЛЬНИК  \n-Заместитель руководителя ОНЭ  \n&#9742; (495) 937-07-44  \n&#128233; melnik-in@ranepa.ru  \n\n ЕКАТЕРИНА ВАСИЛЬЕВНА ПАШТАЛЯН  \n-Начальник учебно-методического отдела ОНЭ  \n&#9742; (495) 937-07-44  \n&#128233; pashtalyan-ev@ranepa.ru '
rekv='Здесь будут отображаться реквизиты'

# Обычные сообщения
def send_msg(user_id, s):
    token.method('messages.send', {'user_id': user_id, 'message': s})
# Обычные сообщения + стикеры
def send_sticker(user_id, s):
    token.method('messages.send', {'user_id': user_id, 'sticker_id': s})


# Тут я задал функцию для отправки сообщения + приложения (из числа уже загруженных вк)
def send_msg_2(user_id, m, add):
    token.method('messages.send', {'user_id': user_id, 'message': m, 'attachment': add})

    
def wiki_list(uid, question):
    wikipedia.set_lang("ru")
    r=wikipedia.search(question)
    spis=''
    if len(r)==0:
        send_msg(uid,'Кажется, не получилось...Отправь 6  чтобы найти что-то еще')
    else:
        for i in range(0,len(r)):
            spis=spis+str(i)+"&#8419;"+"-"+r[i]+'\n'
        send_msg(item["user_id"],"Вот, что удалось найти"+'\n\n'+spis)
    name=uid+'-wiki.txt'
    answers = open(name, 'w')
    answers.write(question)
    answers.close()
    #answers=open(uid+'-wiki.txt', 'w')
    #	answers=open(uid+'.txt', 'w')

def wiki_summ(uid, number):
    wikipedia.set_lang("ru") 
    answers = open(uid+'-wiki.txt', 'r')
    r=wikipedia.search(str(answers.read()))
    title=wikipedia.page(r[int(number)]).title
    summ=wikipedia.summary(r[int(number)], sentences=15)
    url=wikipedia.page(r[int(number)]).url
    send_msg(item["user_id"], '&#128203;'+title+"&#128203;"+'\n\n'+summ+'\n\n'+'Ссылка на статью:'+url)
    answers=open(uid+'-wiki.txt', 'w')
    answers=open(uid+'.txt', 'w')

def nref(name,uid):
    date = time.asctime()
    # Настройки
    mail_sender = 'ranepa.fintech@gmail.com'
    mail_receiver = 'ranepa.fintech@gmail.com'
    username = 'ranepa.fintech@gmail.com'
    password = 'fintechranepa'
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Формируем тело письма
    subject = u'Заказ справки'
    body = u"\n"+name + " "+"-"+" "+"https://vk.com/id"+str(uid)
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # Отпавляем письмо
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(mail_sender, mail_receiver, msg.as_string())
    server.quit()
    send_msg(uid, 'Готово &#128521;')
    
    
def translator(uid,query):
    translator=Translator()
    det=str(translator.detect(query))
    p=det[14:16]
    if p=='ru':
        result=translator.translate(query, dest="en")
    elif p=="en":
        result= translator.translate(query, dest='ru')
    else:
        result= translator.translate(query, dest='ru')
    result=result.text
    send_msg(uid, result)    
    
def keyb(user_id,text,key,msg):
        token.method('messages.send', {'user_id': user_id,'message':str(msg),'keyboard': str(json.dumps(key, ensure_ascii=False))})

#str(ai_msg(user_id, text))        
#APIAI
def ai_msg(uid,text):
    request = apiai.ApiAI('933a88e6eac641918c4e400f34482dee').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = str(text) # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] 
    try:
        send_msg_2(uid,response,'')
    except:
        send_msg_2(uid,'Что-то я совсем Вас не понимаю...','')
        
# Run, motherfucker, run!
def main():
    token = vk_api.VkApi(token='ff813b6f33e6db137cbb43f4fbba6b4f811c8fd16c10b6d00fa4e127e07f29da32cb7d67fed65c53b5349')

    try:
        token._auth_token()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(token)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            uid=str(event.user_id)
            file=uid+'.txt'
            try:
                answers=open(file)
                last_choice=answers.read()
                check=os.stat(uid+'-wiki.txt').st_size == 0
                if int(last_choice[-1:])==1:
                    counter=0
                    if int(event.text)<= 4:
                        schedule(int(event.text))
                        open(file,'w')
                    else:
                        send_msg(uid,'Не знаю такого курса, попробуй еще...')
                    
                elif int(last_choice[-1:])==3:
                    if int(event.text)<= 6:
                        scheme(str(event.text))
                        open(file,'w')
                    else:
                        send_msg(uid,'Кажется, что нас нет такого корпуса, попробуй еще...')
                    
                elif last_choice[-1:]==2:
                    print('yahoooo')
                    nref(str(event.text), str(event.user_id))
                    os.remove(file)
                    
                elif int(last_choice[-1:])==6 and check==True:
                    try:
                        wiki_list(uid,str(event.text))
                        send_msg_2(event.user_id, 'Какая статья тебя интересует? &#128522;\n\n(Ответ может занять несколько секунд, не нервничайте;))', '')
                    except:
                        send_msg(uid,'Не получилось, попробуй перефразировать или спросить что-то попроще...')
                    
                elif int(last_choice[-1:])==6 and check!=True:
                    try:
                        wiki_summ(str(event.text))
                        answers=open(uid+'-wiki.txt', 'w')
                        answers=open(uid+'.txt', 'w')
                    except:
                        send_msg(uid,'Кажется, не получилось...Отправь 6  чтобы найти что-то еще')
                        answers=open(uid+'-wiki.txt', 'w')
                        answers=open(uid+'.txt', 'w')
                    

                elif str(last_choice[-1:])=='7':
                    translator(uid, event.text)
                    open(file,'w')
                    

            except:
                if event.to_me:
                    print('Для меня от: ', end='')
                    print('Текст: ', event.text)
                    if event.text  == 'Привет' or event.text  == 'ку' or event.text  == 'Ку' or event.text  == 'привет' or event.text  == 'Здравствуй' or event.text  == 'здравствуй':
                                send_msg(event.user_id,'Доброго времени суток &#128522;\nЕсли ты знаешь мои команды, то просто выбери нужную или напиши "Помощь", чтобы увидеть список всех команд.')
                                
                    elif event.text  == '1' :
                        print('22')
                        name=uid+'.txt'
                        answers = open(name, 'w')
                        answers.write("1")
                        answers.close()
                        send_msg(event.user_id, 'Какой курс? &#128522;')
                    
                    elif event.text  == '2':
                        
                        send_msg(event.user_id, 'Я уже умею это делать, но давай не будем тревожить деканат, чисто ради теста?&#128519;')
                    elif event.text  == '3':
                        
                        send_msg_2(event.user_id, 'Какой корпус тебе нужен? &#128522;', '')
                        name=uid+'.txt'
                        answers = open(name, 'w')
                        answers.write("3")
                        answers.close()
                    elif event.text  == '4':
                        
                        send_msg(event.user_id, contacts)
                    elif event.text  == 'Как я работаю?':
                        
                        send_msg_2(event.user_id, 'Как-то так &#128517;','video222347_456239086')
                    elif event.text  == '6':
                        
                        send_msg_2(event.user_id, 'Какая статья тебя интересует? &#128522;', '')
                        name=uid+'.txt'
                        answers = open(name, 'w')
                        answers.write("6")
                        answers.close()
                        answers=open(uid+'-wiki.txt', 'w')
                    elif event.text  == 'Перевести':
                        
                        send_msg_2(event.user_id, 'Что будем переводить? &#128522;', '')
                        name=uid+'.txt'
                        answers = open(name, 'w')
                        answers.write("7")
                        answers.close()
                    
                    elif event.text  == "Заказать справку":
                        send_msg(event.user_id, 'Введите ФИО и комментарий.') 
                        name=uid+'.txt'
                        answers = open(name, 'w')
                        answers.write("2")
                        answers.close()
                        
                    elif event.text  == neir:
                       
                        side=random.randint(0,1)
                        coin={0:'Орел',1:'Решка'}                        
                        send_msg(event.user_id, str(coin[side]))
                    elif str(event.text ).lower() == 'сса' or str(event.text ).lower() == 'студсовет':
                        
                        send_msg_2(event.user_id, 'Yo &#128517;','audio2000186416_456240043')
                    elif str(event.text ).lower() == 'спасибо' or str(event.text ).lower() == 'спс' or str(event.text ).lower() == 'сяп':
                        
                        send_sticker(event.user_id, 2047)
                    elif str(event.text ).lower() == 'еще' or str(event.text ).lower() == 'дополнительно':
                        msg='О чем еще меня можно попросить:'
                        keyb(event.user_id,event.text,kbr2, msg)
                    elif str(event.text ).lower() == '<<<<назад' or str(event.text ).lower() =='««Назад' or str(event.text ).lower() == 'меню' :
                        msg='Окей, вот главное меню =)'
                        keyb(event.user_id,event.text,kbr,msg)
                    elif str(event.text ).lower() == 'start':
                        msg='Привет, дружище! \nБуду рад тебе помочь, загляни в меню или просто начни со мной общаться и я попытаюсь ответить что-нибудь осмысленное... &#128517'
                        keyb(event.user_id,event.text,kbr,msg)
                    
                    else:
                        msg=str(ai_msg(event.user_id,event.text))
                        keyb(event.user_id,event.text,kbr,msg)
                        #hz=open('w.txt','a')
                        #hz.write(event.text )
                       # hz.close()
                       # send_msg(event.user_id, 'Кажется, я тебя не понимаю...\nНапиши слово "помощь" или "меню", если еще не знаешь, что я умею или отправь мне команду.')
                       # keyb(event.user_id, kbr)


                if event.from_user:
                    print(event.user_id)

                elif event.from_group:
                    print('группы', event.group_id)

                print('Текст: ', event.text)
            
        else:
            print(event.type, event.raw[1:])
        

if __name__ == '__main__':
    main()
