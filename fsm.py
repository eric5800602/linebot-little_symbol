from transitions.extensions import GraphMachine
from linebot.models import *    
from utils import *
from bs4 import BeautifulSoup
from url_image import url_to_image
from addtext import cv2ImgAddText
from imgurpython import ImgurClient
import requests
import random
import psycopg2
import cv2
import numpy as np
import ast
from dotenv import load_dotenv
   
class TocMachine(GraphMachine):
    load_dotenv()
    client_id = os.getenv("client_id", None)
    client_secret = os.getenv("client_secret", None)
    access_token = os.getenv("access_token",None)
    refresh_token = os.getenv("refresh_token",None)
    global dbpassword
    dbpassword = os.getenv("dbpassword",None)
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def is_going_to_what(self, event):
        text = event.message.text
        return text.lower() == "你會做什麼"
    def is_going_to_image_send(self,event):
        text = event.message.text
        return text.lower() == "來點梗圖"
    def on_enter_image_send(self,event):
        buttons_template = TemplateSendMessage(
        alt_text='各種圖片',
        template=ButtonsTemplate(
            title='各種圖片',
            text='你想看什麼',
            thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
            actions=[
                MessageTemplateAction(
                    label='我的作品',
                    text='我的作品'
                ),
                MessageTemplateAction(
                    label='網路熱門',
                    text='網路熱門'
                ),
                MessageTemplateAction(
                    label='其他人上傳了什麼?',
                    text='其他人上傳了什麼'
                )
            ]
            )
        )
        send_yes_no_button(event.source.user_id,buttons_template)
    def is_going_to_my_works(self,event):
        text = event.message.text
        return text.lower() == "我的作品"
    def on_enter_my_works(self,event):
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_list WHERE user_id = '{0}'".format(event.source.user_id))
        rows = cursor.fetchall()
        for row in rows:
            ro = row[1]
        target = '你的作品有以下：\n\n'
        count = 0
        for i in ro:
            count = count+1
            target += str(count)+'. '+i+'\n\n'
        push_msg(event.source.user_id,target)
        buttons_template = TemplateSendMessage(
        alt_text='我會做：',
        template=ButtonsTemplate(
            title='我會做：',
            text='告訴我能為你做甚麼',
            thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
            actions=[
                MessageTemplateAction(
                    label='網路熱門',
                    text='網路熱門'
                ),
                MessageTemplateAction(
                    label='其他人上傳了什麼',
                    text='其他人上傳了什麼'
                ),
                MessageTemplateAction(
                    label='回到主畫面',
                    text='回到主畫面'
                ),
                MessageTemplateAction(
                    label='我也想貢獻',
                    text='我要貢獻'
                )
            ]
            )
        )
        send_yes_no_button(event.source.user_id,buttons_template)
    #send meme state
    def is_going_to_sendmeme(self, event):
        text = event.message.text
        return text.lower() == "網路熱門"
    def on_enter_sendmeme(self, event):
        print("sendmeme")
        head_Html = 'https://memes.tw/wtf?sort=hot&page='+str(random.randint(1,3))
        res = requests.get(head_Html, timeout=30)
        soup = BeautifulSoup(res.text,'html.parser')
        #print(soup2.prettify())
        imgs = soup.find_all(class_='img-fluid')
        imglist =[]
        target =''
        for img in imgs:
                if 'src' in img.attrs:
                    if img['src'].endswith('.jpg'):
                        imglist.append(img['src'])
        target = random.choice(imglist)
        send_img(event.source.user_id,target)
        buttons_template = TemplateSendMessage(
        alt_text='我會做：',
        template=ButtonsTemplate(
            title='我會做：',
            text='告訴我能為你做甚麼',
            thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
            actions=[
                MessageTemplateAction(
                    label='再來一張',
                    text='再來一張'
                ),
                MessageTemplateAction(
                    label='其他人上傳了什麼',
                    text='其他人上傳了什麼'
                ),
                MessageTemplateAction(
                    label='回到主畫面',
                    text='回到主畫面'
                ),
                MessageTemplateAction(
                    label='我也想貢獻',
                    text='我要貢獻'
                )
            ]
            )
        )
        send_yes_no_button(event.source.user_id,buttons_template)

    def is_going_to_see_others_upload(self, event):
        text = event.message.text
        return text.lower() == "其他人上傳了什麼"
    def on_enter_see_others_upload(self, event):
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_list WHERE user_id != '{0}'".format(event.source.user_id))
        rows = cursor.fetchall()
        row = random.choice(rows)
        send_img(event.source.user_id,random.choice(row[1]))
        buttons_template = TemplateSendMessage(
        alt_text='我會做：',
        template=ButtonsTemplate(
            title='我會做：',
            text='告訴我能為你做甚麼',
            thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
            actions=[
                MessageTemplateAction(
                    label='再來一張',
                    text='再來一張'
                ),
                MessageTemplateAction(
                    label='網路熱門',
                    text='網路熱門'
                ),
                MessageTemplateAction(
                    label='回到主畫面',
                    text='回到主畫面'
                ),
                MessageTemplateAction(
                    label='我也想貢獻',
                    text='我要貢獻'
                )
            ]
            )
        )
        send_yes_no_button(event.source.user_id,buttons_template)
    
    def is_going_to_image_send_again(self,event):
        text = event.message.text
        return text.lower() == "再來一張"
    def is_going_to_main(self,event):
        text = event.message.text
        if text.lower() == "回到主畫面":
            push_msg(event.source.user_id,"已回到主畫面")
        return text.lower() == "回到主畫面"
    def on_enter_fsm(self, event):
        print("I'm entering fsm")

        reply_token = event.reply_token
        send_image_url(reply_token,"https://symbol-linebot.herokuapp.com/show-fsm")
        self.go_back()


    def on_enter_what(self, event):
        print("I'm entering what")
        reply_token = event.reply_token
        buttons_template = TemplateSendMessage(
        alt_text='我會做：',
        template=ButtonsTemplate(
            title='我會做：',
            text='告訴我能為你做甚麼',
            thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
            actions=[
                MessageTemplateAction(
                    label='讓你看看我的fsm',
                    text='fsm'
                ),
                MessageTemplateAction(
                    label='來點正能量吧',
                    text='來點梗圖'
                ),
                MessageTemplateAction(
                    label='製作梗圖',
                    text='我要貢獻'
                ),
                MessageTemplateAction(
                    label='模板增加',
                    text='貢獻模板'
                )
                ]
            )
        )
        send_yes_no_button(event.source.user_id,buttons_template)
        self.go_back()

    def is_going_to_create_img(self,event):
        text = event.message.text
        if text.lower() == "我要貢獻":
            global offset
            offset = 0
        return text.lower() == "我要貢獻" 
    
    def on_enter_create_img(self,event):
        print("I'm entering create_img")
        reply_token = event.reply_token
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_template order by index LIMIT 10 offset "+str(offset))
        rows = cursor.fetchall()
        target = ''
        count = offset
        for row in rows:
            count=count+1
            target += (str(count) + ". "+str(row[0])+"\n貢獻者："+str(row[5])+"\n")
        print("target:"+str(offset)+'\n')
        global number_of_template
        cursor.execute("SELECT COUNT ('id') FROM image_template")
        rows = cursor.fetchall()
        for row in rows:
            number_of_template = row[0]
        conn.commit()
        cursor.close()
        conn.close()
        push_msg(event.source.user_id,"請選擇你想要的模板\n總共有{0}筆模板\n".format(number_of_template)+target+"\n輸入 下一頁 換頁 \n輸入 上一步 回到上一步")
        #send img list

    def on_exit_create_img(self,event):
        print("exist create_img")
    def is_going_to_next_page(self,event):
        get = False
        if event.message.text == "下一頁":
            global offset
            offset += 10
            if(number_of_template > offset):
                get = True
            else:
                push_msg(event.source.user_id,"沒有下一頁了啦")
        return get
    def is_going_to_choose_template(self,event):
        text = event.message.text
        target = False
        if(text.isdigit()):
            target = True
            if(int(text) > number_of_template):
                push_msg(event.source.user_id,"我還沒那麼多")
                target = False    
            global target_template
            target_template = int(text)
        return target
    
    def on_enter_choose_template(self,event):
        print("I'm entering choose_template")
        text = event.message.text
        reply_token = event.reply_token
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_template order by index")
        rows = cursor.fetchall()
        target = ''
        count = 0
        global number_of_current_text
        for row in rows:
            count=count+1
            target = row[1]
            number_of_current_text = row[3]
            if(count == target_template):
                break
        conn.commit()
        cursor.close()
        conn.close()
        #send image
        push_msg_img(event.source.user_id,target,"請依照順序填入你要的文字\n**這裡有 {0} 串字**\n".format(number_of_current_text)+"範例：(系統說有3個字)\n文字1 文字2 文字3\n\n輸入 上一步 回到上一步")
        

    def on_exit_choose_template(self,event):
        print("exist choose_template")
    
    def is_going_to_initial(self,event):
        text = event.message.text
        reply_token = event.reply_token
        if text.lower() == "上一步":
            send_text_message(reply_token,"是的船長 已回到上一步")
        return text.lower() == "上一步"
    def is_going_to_confirm(self,event):
        text = event.message.text
        strt = text.split()
        ret = False
        if (len(strt) == number_of_current_text):
            ret = True
        else:
            push_msg(event.source.user_id,"你輸入的太少囉")
        #split text
        return ret

    def on_enter_confirm(self,event):
        print("I'm entering confirm")
        reply_token = event.reply_token
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        print("Connection established")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_template order by index")
        rows = cursor.fetchall()
        text = event.message.text
        text = text.split()
        global text_record
        text_record = text
        print(text)
        target =''
        x = []
        y = []
        num = 0
        count = 0
        for row in rows:
            count=count+1
            target = row[2] #original url
            num = row[3] #number of text
            pos = row[4]
            if(count == target_template):
                break
        print(target)
        global img
        img = url_to_image(target)
        res = ast.literal_eval(pos)
        for i in range(num):
            img = cv2ImgAddText(img,text[i],res[i][0],res[i][1],(255,255,255),30)
        conn.commit()
        cursor.close()
        conn.close()
        cv2.imwrite(str(id)+".png", img )
        Confirm_template = TemplateSendMessage(
        alt_text='目錄',
        template=ConfirmTemplate(
            title='Confirm',
            text='這樣可以嗎',
            actions=[                              
                PostbackTemplateAction(
                    label='Yes',
                    text='Yes',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='No',
                    text='No'
                )
            ]
        )
        )
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        global url
        url = client.upload_from_path(str(id)+".png", config=None, anon=False)
        os.remove(str(id)+".png")
        send_img(event.source.user_id,url['link'])
        send_yes_no_button(event.source.user_id,Confirm_template)
        global fix_index
        global fix_index2
        global fix_index3
        fix_index = False
        fix_index2 = False
        fix_index3 = False
    
    def is_going_to_return(self,event):
        text = event.message.text
        user_id = event.source.user_id
        if text.lower() == "yes":
            push_msg(event.source.user_id,"已儲存在資料庫")
            push_msg(event.source.user_id,"網址在這請小心服用\n" + url['link'])
            conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
            print("Connection established")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO image_list(user_id) VALUES ('{id}') ON CONFLICT (user_id) DO UPDATE SET user_id = ('{id}');\
            UPDATE image_list\
            SET url = array_cat(url,'{{{link}}}')\
            Where \"user_id\" = ('{id}');".format(id = user_id,link = url['link']))
            conn.commit()
            cursor.close()
            conn.close()
        return text.lower() == "yes"
    
    def is_going_to_which_needfix(self,event):
        text = event.message.text
        return text.lower() == "no"
    def on_enter_which_needfix(self,event): 
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
                title='哪裡不好你跟我說',
                text='告訴我你覺得哪裡不好',
                actions=[
                    MessageTemplateAction(
                        label='修改文字',
                        text='修改文字',
                    ),
                    MessageTemplateAction(
                        label='修改字體顏色',
                        text='修改字體顏色'
                    ),
                    MessageTemplateAction(
                        label='修改字體大小',
                        text='修改字體大小'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/2zh0E28.png',
                title='哪裡不好你跟我說',
                text='告訴我你覺得哪裡不好',
                actions=[
                    MessageTemplateAction(
                        label='修改字體位置',
                        text='修改字體位置'
                    ),
                    MessageTemplateAction(
                        label='更改模板',
                        text='我要貢獻'
                    ),
                    MessageTemplateAction(
                        label='回到主畫面',
                        text='回到主畫面'
                    )
                ]
            )
        ]
        )
        )   
        send_yes_no_button(event.source.user_id,Carousel_template)
    def is_going_to_fix_text(self,event):
        text = event.message.text
        return text.lower() == "修改文字"
    def is_going_to_adjust(self,event):
        text = event.message.text
        return text.lower() == "修改字體顏色" or text.lower() == "修改字體大小" or text.lower() == "修改字體位置"
    def on_enter_adjust(self,event):
        text = event.message.text
        global fix_index
        global fix_index2
        global fix_index3
        if(text.lower() == "修改字體顏色"):
            push_msg(event.source.user_id,"請輸入你想要顏色(r,g,b)\n範例：\n255 255 255")
            fix_index = True
        if(text.lower() == "修改字體大小"):
            push_msg(event.source.user_id,"請輸入字體大小\n範例：\n30")
            fix_index2 = True
        if(text.lower() == "修改字體位置"):
            push_msg(event.source.user_id,"請輸入修改字體資訊\n範例：\nx 加(減) 100 y 加(減) 0")
            fix_index3 = True
    def is_going_to_confirm_again(self,event):
        text = event.message.text
        get = True
        get2= True
        get3= True
        if(fix_index):
            text = text.split()
            print(len(text))
            for i in text:
                if(not i.isdigit()):
                    get = False
                    break
            if(len(text) != 3):
                get = False
            if(get):
                global r,g,b
                r = text[0]
                g = text[1]
                b = text[2]
        text = event.message.text
        if(fix_index2):
            get2 = text.isdigit()
            if(get2 and len(text.split()) == 1):
                global fontsize
                fontsize = int(text)
                print(fontsize)
        text = event.message.text
        if(fix_index3):
            text = text.split()
            if(len(text) == 6):
                if(text[0] == "x" and text[3] == "y" and (text[1] == "加" or text[1] =="減") and (text[4] == "加" or text[4] =="減")):
                    get3 = True
                    global x_shift,y_shift
                    x_shift = 0
                    y_shift = 0
                    if(text[1] == "加"):
                        x_shift = int(text[2]) + x_shift
                    elif(text[1] == "減"):
                        x_shift -= int(text[2])
                    if(text[4] == "加"):
                        y_shift += int(text[5])
                    elif(text[4] == "減"):
                        y_shift -= int(text[5])
                else:
                    get3 = False
            else:
                get3 = False
        return get or get2 or get3
    def on_enter_confirm_again(self,event):
        print("I'm entering confirm again")
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        print("Connection established")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM image_template order by index")
        rows = cursor.fetchall()
        text = event.message.text
        text = text.split()
        color = (255,255,255)
        fs = 30
        xs = 0
        ys = 0
        target =''
        x = []
        y = []
        num = 0
        count = 0
        for row in rows:
            count=count+1
            target = row[2] #original url
            num = row[3] #number of text
            pos = row[4]
            if(count == target_template):
                break
        print(target)
        if(fix_index):
            color = (int(r),int(g),int(b))
        if(fix_index2):
            fs = fontsize
        if(fix_index3):
            global x_shift
            global y_shift
            xs += x_shift
            ys += y_shift
        global img
        img = url_to_image(target)
        res = ast.literal_eval(pos)
        for i in range(num):
            img = cv2ImgAddText(img,text_record[i],res[i][0]+xs,res[i][1]+ys,color,fs)
        conn.commit()
        cursor.close()
        conn.close()
        cv2.imwrite(str(id)+".png", img )
        Confirm_template = TemplateSendMessage(
        alt_text='目錄',
        template=ConfirmTemplate(
            title='Confirm',
            text='這樣可以嗎',
            actions=[                              
                PostbackTemplateAction(
                    label='Yes',
                    text='Yes',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='No',
                    text='No'
                )
            ]
        )
        )
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        global url
        url = client.upload_from_path(str(id)+".png", config=None, anon=False)
        os.remove(str(id)+".png")
        send_img(event.source.user_id,url['link'])
        send_yes_no_button(event.source.user_id,Confirm_template)

    def is_going_to_input_username(self,event):
        text = event.message.text
        return text.lower() == "貢獻模板"
    def on_enter_input_username(self,event):
        push_msg(event.source.user_id,"輸入你的暱稱\n 範例：小蓁")
    def is_going_to_add_template(self,event):
        if isinstance(event.message, TextMessage):
            global username
            username = event.message.text
            get = True
        else:
            push_msg(event.source.user_id,"你連傳打字給我都不會嗎")
        return get
    def on_enter_add_template(self,event):
        push_msg(event.source.user_id,"讓我看看他原本的樣子")
    def on_exit_add_template(self,event):
        print('exit add_template')

    def is_going_to_get_image(self,event):
        get = False
        if isinstance(event.message, ImageMessage):
            get = True
        else:
            push_msg(event.source.user_id,"你連傳圖片給我都不會嗎")
        return get
    def on_enter_get_image(self,event):
        global upimg
        global width
        global height
        [upimg,width,height] = upload_img(event)
        push_msg(event.source.user_id,"現在傳給我模板圖片,他必須有號碼標示")
    def on_exit_get_image(self,event):
        print('exit get_image')
    
    def is_going_to_get_image2(self,event):
        get = False
        if isinstance(event.message, ImageMessage):
            get = True
        else:
            push_msg(event.source.user_id,"你連傳圖片給我都不會嗎")
        return get
    def on_enter_get_image2(self,event):
        global upimg2
        [upimg2,width2,height2] = upload_img(event)
        push_msg(event.source.user_id,"為他起個名字吧,並決定文字格子數量以及位置後確認上傳\n形式：\n標題 文字格子數量 位置1x 位置1y 位置2x 位置2y ......\n範例：\n亞洲人之恥 3 20 190 120 417 155 625")
    def on_exit_get_image2(self,event):
        print('exit get_image')

    def is_going_to_decide_format(self,event):
        text = event.message.text
        text = text.split()
        if(len(text)-2 != int(text[1])*2):
            push_msg(event.source.user_id,"你的格式有點問題ㄋㄟ,請重新輸入")
            return False
        else:
            return True
    def on_enter_decide_format(self,event):
        text = event.message.text
        text = text.split()
        path = []
        for i in range(2,int(text[1])*2+2,2):
            path.append(tuple([int(text[i]),int(text[i+1])]))
        conn = psycopg2.connect(database="dde2dm8s4unot",user="suxfxobluvhxtc",password=dbpassword,host="ec2-174-129-205-197.compute-1.amazonaws.com",port ="5432")
        print("Connection established")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT ('id') FROM image_template")
        rows = cursor.fetchall()
        for row in rows:
            index = row[0]
        cursor.execute("INSERT INTO image_template (name,url,original_url,count,site,\"user\",index)\
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(text[0],upimg2['link'],upimg['link'],int(text[1]),path,username,index))
        conn.commit()
        cursor.close()
        conn.close()
        push_msg(event.source.user_id,"上傳成功")
        Confirm_template = TemplateSendMessage(
        alt_text='目錄',
        template=ConfirmTemplate(
            title='Confirm',
            text='現在要幹嘛',
            actions=[                              
                PostbackTemplateAction(
                    label='回到主畫面',
                    text='回到主畫面',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='再來一次',
                    text='再來一次'
                )
            ]
        )
        )
        send_yes_no_button(event.source.user_id,Confirm_template)
    def on_exit_decide_format(self,event):
        print('exit get_image')
    
    def is_going_to_goback_from_decide_format(self,event):
        text = event.message.text
        push_msg(event.source.user_id,"已回到主畫面")
        return text.lower() == "回到主畫面"
    def is_going_to_add_template_again(self,event):
        text = event.message.text
        return text.lower() == "再來一次"
    