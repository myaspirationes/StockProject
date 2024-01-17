# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 19:45
@Auth ： Tiger
@File ：weibo_ablum.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
import requests
import time,os




header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Referer": f"https://weibo.com",
    'cookie':'SINAGLOBAL=192321401298.90274.1628520195961; UOR=,,www.baidu.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5zhH1GAhZZ4Pjq1J6J.CIW5JpX5KMhUgL.FozXSoBRSKeNe0B2dJLoIEXLxKML1heL1-qLxKqLBo5LBoBLxK.L1KMLBoBLxK-L12-LB.zLxKBLB.2L1hqt; XSRF-TOKEN=4K3c_SJQT2nlhl6iAh9jQLix; ALF=1698223929; SSOLoginState=1695631929; SCF=Av4F9lUsw2cJEfjqiusK4yQpnPW7GP3KrdoyuX5TqGNI5VIkAqsSN949BV-thNwlVgjX3Vh2lR_IRfbV8TDz0lA.; SUB=_2A25IFTpqDeRhGeRK7VYZ9S3LyDiIHXVrYyyirDV8PUNbmtANLVjSkW9NU33QkwXa63DHCH2DIUIORwGZ31h9TIyG; _s_tentry=weibo.com; Apache=1210166956977.9138.1695631942130; ULV=1695631942257:177:11:2:1210166956977.9138.1695631942130:1695531220197; WBPSESS=Z8Jz2InUi7Z7ZSkpzBTYzsb0rXLBjV3s-vDKI2tOTan_XXz9Xmn2IHbLZhBalRNmyzmwMUAAcYcpUaTj4DZP6JSc3v87YRwTZM6KSMXI-p9JS5UE4O4CC8jVn57wFbBn9x9UNAQtSqGXooAa7sp6sA=='
}

uid="5307758821"


# 92eaaee6ly1gtfa3texbbj22083kghdw
def picture_save(i,last_pid):
    pid = i['pid']

    # wap360、orj960、large和mw2000 表示图片的大小，依次递增
    picture_url = f'https://wx4.sinaimg.cn/large/{pid}.jpg'
    picture_rep = requests.get(url=picture_url, headers=header)
    # print(pid)
    url2 = f'{path}/{pid}.jpg'
    if not os.path.exists(url2):
        with open(url2, 'wb') as f:
            f.write(picture_rep.content)
    if pid==last_pid:
        exit()

def get_weibo_picture(uid):


    url1 = f'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid=0&has_album=true'

    request_header = requests.get(url=url1, headers=header)
    html = request_header.json()
    next_page = html['data']['since_id']  # 下一页
    picture = html['data']['list']
    print(picture)
    last_pid=picture[-1]['pid']
    url2 = f'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid={next_page}'
    foronce = 1

    for i in picture:
        # 暂停3秒 防止访问太过平凡，被识别恶意攻击封掉ip，所以添加了time。sleep()等待3秒在爬取
        time.sleep(3)
        picture_save(i,last_pid)
        # print("helwl")

        for ls in range(8):

            # 暂停3秒
            time.sleep(3)
            print(url2)
            print("slide to next page.....")

            #防止网络中断后重头下载,
            # if foronce==1:
            #     url2='https://weibo.com/ajax/profile/getImageWall?uid=5307758821&sinceid=4924560700211850_-1_20230718_-1'
            # foronce=2

            request1 = requests.get(url=url2, headers=header)
            html1 = request1.json()
            next_page1 = html1['data']['since_id']
            picture = html1['data']['list']
            print(picture)
            url2 = f'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid={next_page1}'
            for a in picture:
                # 暂停3秒
                time.sleep(1)
                picture_save(a,last_pid)
                # print("pid")
                




if __name__ == '__main__':

    path = f'D:/Downloads/weibo/{uid}'
    if not os.path.exists(path):
        os.makedirs(path)
    get_weibo_picture(uid)