import pymysql
import time as t
from tkinter  import messagebox#사이즈를 재설정하기 위해서 사용 PIL TOOLS인스톨
from tkinter import *

#로그인
def login(id,password):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sql=f"select * from 고객"
    cur.execute(sql)
    res = cur.fetchall()
    admin=False
    isLogin=False
    for i in res:
        if i[1] == id:
            if i[2] == password:
                if  i[8]=='관리자':
                    admin=True
                isLogin=True

    if isLogin:
        return isLogin,admin
    else:
        return isLogin,False
#고객번호
def userNume(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sql=f"select 고객번호 from 고객 where id = '{id}';"
    cur.execute(sql)
    res = cur.fetchall()
    return res


def buyHistory(id): #구매내역 출력
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sql = f"select id, 상품명, 판매날짜 from 고객, 상품, 판매, 판매상세 where 고객.고객번호=판매.고객번호 and 판매.판매번호=판매상세.판매번호 and 판매상세.상품번호=상품.상품번호 and id='{id}';"
    cur.execute(sql)
    res = cur.fetchall()
    print(res)


def selectSale():
    return f'select 상품번호, 상품명, 판매가 from 상품;'
def selectUP():
    return f'select 상품번호, 상품명, 판매가, 원가 from 상품;'

#상품목록
def productsList(info):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlProList = info
    cur.execute(sqlProList)
    res = cur.fetchall()
    return res


def time():
    time = t.strftime('%Y-%m-%d %H:%M:%S')
    return time

#판매 인서트
def saleInsert(userVal):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlInsert=f"insert into 판매(판매날짜, 고객번호) values ('{time()}','{userVal}');"#판매에 insert
    cur.execute(sqlInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영

def newpack(x):
    for i in list:
        i.pack_forget()

    list[x].pack()

##상품 인서트 함수
def insertPro(pName, sPrice, rPrice):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlProductInsert = f"insert into 상품(상품명, 판매가, 원가) values ('{pName}','{sPrice}','{rPrice}');"  # 상품추가 insert
    cur.execute(sqlProductInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영
#상품 삭제
def delete(delPro):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqldelete = f"delete from 상품 where 상품명='{delPro}';"
    cur.execute(sqldelete)
    conn.commit()

#상품업데이트
def update_pro(sale_PR, real_PR, pName):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlProductUpdate = f"UPDATE 상품 SET 판매가='{sale_PR}',원가='{real_PR}' WHERE 상품명='{pName}';"
    cur.execute(sqlProductUpdate)
    conn.commit()

def newACInsert(id, password, sex, add, addNum, phone, phone2, iden):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlInsert=f"insert into 고객(id, pass, 성별, 주소, 우편번호, 전화번호, 휴대번호, 구분) values ('{id}','{password}', '{sex}', '{add}', '{addNum}', '{phone}', '{phone2}', '{iden}');"#판매에 insert
    cur.execute(sqlInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영

def selectProNum(time, userVal):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlSale = f"select 판매번호 from 판매 where 판매날짜 like '%{time}%' and 고객번호 like {userVal};"  # 판매상세에 insert트 하기 위해서 판매 번호를 출력하기 위한 과정
    cur.execute(sqlSale)
    resSale = cur.fetchall()
    return resSale

#판매 상세 인서트
def saleList(saleNume, proNume, proCount):
    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='상품판매db', charset='utf8')
    cur = conn.cursor()
    sqlSaleInsert = f"insert into 판매상세(판매번호, 상품번호, 수량) values ({saleNume},{proNume},{proCount});"  # 판매상세 insert
    cur.execute(sqlSaleInsert)
    conn.commit()  # 처리된 내용을 판매 테이블에 반영
