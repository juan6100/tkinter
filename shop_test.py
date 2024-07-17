import os
import sys
from tkinter  import messagebox#사이즈를 재설정하기 위해서 사용 PIL TOOLS인스톨
from tkinter import *
import pymysql
import login_code as LC
import time as t

def resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

value=None
adminValue=None
proRes=LC.productsList(LC.selectSale())#리스트 박스를 위한 상품 목록

def list():
    list_for_update=LC.productsList(LC.selectUP())
    return list_for_update

canList=[]
userNum=0
ID=None

#화면전환 함수
def newpack(x):
    for i in canList:
        i.pack_forget()

    canList[x].pack()

#로그인 성공시 다음으로 넘기는 함수
def login_text():
    global userNum
    islogin,isadmin=LC.login(is_login_entry.get(), is_password_entry.get())
    if islogin and isadmin:
        newpack(2)
        userNum=LC.userNume(is_login_entry.get())[0][0]
        print(userNum)


    elif islogin and not isadmin:
        newpack(1)
        userNum = LC.userNume(is_login_entry.get())[0][0]


    else:
        messagebox.showinfo("오류","다시 입력하시오")


#구매 클릭시에 넘어가는 함수
def saleMenu():
    newpack(3)
    btBack = Button(buy_newCan, text="뒤로가기", command=login_text)
    btBack.place(x=10, y=350)


def show_sale_list():
    newpack(4)
    buyHistory(userNum)
    makeBox()
    btBack = Button(sale_history_newCan5, text="뒤로가기", command=login_text)
    btBack.place(x=10, y=350)


def update():
    newpack(5)
    btBack = Button(update_newCan, text="뒤로가기", command=login_text)
    btBack.place(x=10, y=350)
    makeLB(update_newCan)


def insert():
    newpack(6)
    btBack = Button(insert_newCan, text="뒤로가기", command=login_text)
    btBack.place(x=10, y=350)


def delete():
    newpack(7)
    btBack = Button(delete_newCan, text="뒤로가기", command=login_text)
    btBack.place(x=10, y=350)
    makeLB(delete_newCan)



def makeAC():
    newpack(8)
    btBack = Button(makeNewAC_newCan, text="뒤로가기", command=lambda : newpack(0))
    btBack.place(x=10, y=350)


w=Tk()
w.geometry("400x400")


#로그인 페이지 켄버스
is_login_newCan=Canvas(w, width=400, height=400)
is_login_entry = Entry(is_login_newCan)
is_login_entry.insert(0,'도우너')
is_password_entry = Entry(is_login_newCan)
is_password_entry.insert(0,'1234')
is_login_bt1=Button(is_login_newCan, text="로그인", command=login_text)
make_ACbt=Button(is_login_newCan, text="회원가입", command=makeAC)
ID=is_login_entry.get()
is_id_label=Label(is_login_newCan, text="ID")
is_pass_label=Label(is_login_newCan, text="PASS")



is_id_label.place(x = 120, y = 170)
is_pass_label.place(x = 110, y = 200)#padx 가로 위치 조절
is_login_entry.place(x=150, y=170)
is_password_entry.place(x=150, y=200)
is_login_bt1.place(x=180, y=250)
make_ACbt.place(x=300, y=350)
canList.append(is_login_newCan)

#사용자 메뉴 켄버스
user_Menu_newCan=Canvas(w, width=400, height=400, background="red")
bt2=Button(user_Menu_newCan, text="구매", command=saleMenu)
bt3=Button(user_Menu_newCan, text="구매내역", command=show_sale_list)
bt2.place(x=180, y=200)#구매
bt3.place(x=180, y=250)#구매
canList.append(user_Menu_newCan)
btBack = Button(user_Menu_newCan, text="뒤로가기", command= lambda : newpack(0))
btBack.place(x=10, y=350)



#관리자 메뉴 켄버스
admin_newCan=Canvas(w, width=400, height=400, background="green")
bt4=Button(admin_newCan, text="상품 수정", command=update)
bt5=Button(admin_newCan, text="상품 추가", command=insert)
bt6=Button(admin_newCan, text="상품 삭제", command=delete)
bt4.place(x=180, y=150)
bt5.place(x=180, y=200)
bt6.place(x=180, y=250)
btBack = Button(admin_newCan, text="뒤로가기", command= lambda : newpack(0))
btBack.place(x=10, y=350)
canList.append(admin_newCan)




###구매 목록을  리스트박스로 표현
buy_newCan=Canvas(w, width=400, height=400)
canList.append(buy_newCan)
def pro_choice(event):
    global value
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)


def get_proNum(value):
    newV=value
    newV = newV.replace('(', '')
    newV = newV.replace(' ', '')
    newV = newV.replace(')', '')
    newV = newV.split(",")
    return newV


def getValue(productsEA):
    global userNum
    time = t.strftime('%Y-%m-%d')
    saleInsert(time, userNum)
    saleNum=selectProNum(time, userNum)
    proNume=get_proNum(value)
    n=int(len(saleNum))
    saleList(saleNum[n-1][0],proNume[0],productsEA)
    messagebox.showinfo("구매완료", "구매완료")
    login_text()

#판매인서트
def saleInsert(time,userVal):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlInsert = f"insert into 판매(판매날짜, 고객번호) values ('{time}','{userVal}');"  # 판매에 insert
    cur.execute(sqlInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영

#판매번호
def selectProNum(time, userVal):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlSale = f"select 판매번호 from 판매 where 판매날짜 like '%{time}%' and 고객번호 like {userVal};"  # 판매상세에 insert트 하기 위해서 판매 번호를 출력하기 위한 과정
    cur.execute(sqlSale)
    resSale = cur.fetchall()
    return resSale

#판매 상세 인서트
def saleList(saleNume, proNume, proCount):
    print(saleNume)
    print(proNume)
    print(proCount)

    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlSaleInsert = f"insert into 판매상세(판매번호, 상품번호, 수량) values ({saleNume},{proNume},{proCount});"  # 판매상세 insert
    cur.execute(sqlSaleInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영

#리스트 박스 생성
products_listbox = Listbox(buy_newCan, selectmode='extended', height=10)
products_listbox.bind('<<ListboxSelect>>', pro_choice)


#리스트 박스 여러개 출력
for x in range(len(proRes)):
    products_listbox.insert(x, str(proRes[x]))
products_listbox.place(x=120, y=20)

countL=Label(buy_newCan, text="수량 입력:")
products_count_entry=Entry(buy_newCan)
products_count_entry.place(x=150, y=200, width=50)
countL.place(x=90, y=200, width=50)

purchase_bnt=Button(buy_newCan, text="구매", command=lambda : getValue(products_count_entry.get()))#command=click_button)
purchase_bnt.place(x=220, y=200)





#구매내역
sale_history_newCan5=Canvas(w, width=400, height=400, background="blue")
canList.append(sale_history_newCan5)


def buyHistory(userNum): #구매내역 출력
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sql = f"select id, 상품명, 판매날짜 from 고객, 상품, 판매, 판매상세 where 고객.고객번호=판매.고객번호 and 판매.판매번호=판매상세.판매번호 and 판매상세.상품번호=상품.상품번호 and 고객.고객번호='{userNum}';"
    cur.execute(sql)
    res = cur.fetchall()
    return res

def makeBox():
    sale_history_box = Listbox(sale_history_newCan5, selectmode='extended', height=15, width=40 )

    for x in range(len(buyHistory(userNum))):
        sale_history_box.insert(x, str(buyHistory(userNum)[x]))
    sale_history_box.place(x=50, y=50)
    sale_history_box.bind('<<ListboxSelect>>')


#상품 수정
update_newCan=Canvas(w, width=400, height=400)
canList.append(update_newCan)

def pro_choice_SP(event):
    global adminValue
    w = event.widget
    index = int(w.curselection()[0])
    prime_value = w.get(index)
    prime_value=prime_value.replace('(','')
    prime_value = prime_value.replace(' ', '')
    prime_value=prime_value.replace(')','')
    adminValue=prime_value.split(",")

    print(value,type(value), value[1].strip("'"))


#판매가 원가 수정

#리스트박스 생성
def makeLB(canvas):
    products_listboxInU = Listbox(canvas, selectmode='extended', height=7, width=25)
    products_listboxInU.bind('<<ListboxSelect>>', pro_choice_SP)

    ##리스트박스 여러개 출력
    for x in range(len(list())):
        products_listboxInU.insert(x, str(list()[x]))
    products_listboxInU.place(x=80, y=100)

def is_value_for_update():
    pName = adminValue[1].strip("'")
    sprice=salePrice_entry.get()
    rprice=realPrice_entry.get()
    LC.update_pro(sprice,rprice,pName)
    messagebox.showinfo("완료", "성공적으로 수정되었습니다.")
    products_listbox.forget()
    makeLB(update_newCan)


##entry랑 버튼만드는 함수

salePrice_label=Label(update_newCan,text="판매가: ")
realPrice_label=Label(update_newCan, text="원가: ")
salePrice_label.place(x=60, y=300)
realPrice_label.place(x=185, y=300)
salePrice_entry=Entry(update_newCan)
realPrice_entry=Entry(update_newCan)
salePrice_entry.place(x=110, y=300, width=50)
realPrice_entry.place(x=220, y=300, width=50)
confirm_bnt=Button(update_newCan, text="수정", command=is_value_for_update)#command=click_button)
confirm_bnt.place(x=300, y=300)



#상품 추가
insert_newCan=Canvas(w, width=400, height=400)
canList.append(insert_newCan)

products_Name_label = Label(insert_newCan, text="상품명: ")
products_salePrice_label=Label(insert_newCan,text="판매가: ")
products_realPrice_label=Label(insert_newCan, text="원가: ")
products_Name_label.place(x=60, y=200)
products_salePrice_label.place(x=60, y=300)
products_realPrice_label.place(x=185, y=300)
products_Name_emtry=Entry(insert_newCan)
products_salePrice_entry=Entry(insert_newCan)
products_realPrice_entry=Entry(insert_newCan)
products_Name_emtry.place(x=110, y=200, width=50)
products_salePrice_entry.place(x=110, y=300, width=50)
products_realPrice_entry.place(x=220, y=300, width=50)

def insertProd():
    pName = products_Name_emtry.get()
    sPrice = products_salePrice_entry.get()
    rPrice = products_realPrice_entry.get()
    LC.insertPro(pName,sPrice,rPrice)
    messagebox.showinfo("입력 완료", "성공적으로 추가되었습니다.")


confirm_bnt=Button(insert_newCan, text="입력", command=insertProd)
confirm_bnt.place(x=300, y=300)

###상품 삭제
delete_newCan=Canvas(w, width=400, height=400)
canList.append(delete_newCan)

def is_name_for_delete():
    delPro=adminValue[1].strip("'")
    LC.delete(delPro)
    print(delPro)
    messagebox.showinfo("삭제 완료", "삭제되었습니다.")
    products_listbox.forget()
    makeLB(delete_newCan)

confirm_bnt=Button(delete_newCan, text="삭제", command=is_name_for_delete)
confirm_bnt.place(x=300, y=300)


#회원가입
makeNewAC_newCan=Canvas(w, width=400, height=400)
canList.append(makeNewAC_newCan)

#라벨
userid_label = Label(makeNewAC_newCan, text="ID: ")
userPS_label=Label(makeNewAC_newCan,text="PASSWORD: ")
sex_label=Label(makeNewAC_newCan, text="성별: ")
add_label=Label(makeNewAC_newCan, text="주소: ")
addNum_label=Label(makeNewAC_newCan, text="우편번호: ")
phone_label=Label(makeNewAC_newCan, text="전화번호: ")
phone2_label=Label(makeNewAC_newCan, text="휴대번호: ")
userid_label.place(x=150, y=20)
userPS_label.place(x=96, y=50)
sex_label.place(x=138, y=80)
add_label.place(x=138, y=110)
addNum_label.place(x=115, y=140)
phone_label.place(x=115, y=170)
phone2_label.place(x=115, y=200)

#엔트리
userid_entry=Entry(makeNewAC_newCan)
userPS_entry=Entry(makeNewAC_newCan)
sex_entry=Entry(makeNewAC_newCan)
add_entry=Entry(makeNewAC_newCan)
addNum_entry=Entry(makeNewAC_newCan)
phone_entry=Entry(makeNewAC_newCan)
phone2_entry=Entry(makeNewAC_newCan)
userid_entry.place(x=170, y=20)
userPS_entry.place(x=170, y=50)
sex_entry.place(x=170, y=80, width=100)
add_entry.place(x=170, y=110)
addNum_entry.place(x=170, y=140)
phone_entry.place(x=170, y=170)
phone2_entry.place(x=170, y=200)

def getting_user_val():
    checkList=[]
    id=userid_entry.get()
    checkList.append(id)
    password=userPS_entry.get()
    checkList.append(password)
    sex=sex_entry.get()
    checkList.append(sex)
    add=add_entry.get()
    checkList.append(add)
    addNum=addNum_entry.get()
    checkList.append(addNum)
    phone=phone_entry.get()
    checkList.append(phone)
    phone2=phone2_entry.get()
    checkList.append(phone2)
    print(len(checkList))
    if "" in checkList:
        messagebox.showinfo("오류", "빈칸없이 다시 입력하시오")
    else:
        LC.newACInsert(id, password, sex, add, addNum, phone, phone2, '사용자')
        messagebox.showinfo("완료", "회원가입이 완료되었습니다!")
        newpack(0)

MAbt=Button(makeNewAC_newCan, text="입력", command=getting_user_val)
MAbt.place(x=170, y=240)


is_login_newCan.pack()
w.mainloop()



