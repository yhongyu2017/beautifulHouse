# urllib.request 模块提供了最基本的构造 HTTP 请求的方法，利用它可以模拟浏览器的一个请求发起过程，

# 导入请求模块
import urllib.request  # urllib.request可以用来发送request和获取request的结果
from lxml import etree  # 用来处理html代码库解析html文本
import ssl  # 使用ssl创建未经验证的上下文，在urlopen中传入上下文参数
import uuid  # 使用uuid生成全球唯一id
from getInfo.connect_db import ConnectDb  # 导入自定义连接数据库类

ssl._create_default_https_context = ssl._create_unverified_context


class AnJuKe(object):
    # 创建网址属性
    def __init__(self,url):
        # 初始化url
        self.url=url

    def get_data(self):
        try:
            # 这块为请求头通过修改 User - Agent来伪装成浏览器，默认的User - Agent是 Python - urllib
            # 通过修改它来伪装浏览器
            page_headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
                          "Cookie":"lps=http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fwww.baidu.25B1%2585%25E5%25AE%25A2%26rsv_spt%3D1%26rsv_iqid%3D0xcd19993e00074b01%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3D%26tn%3Dbaiduhome_pg%26ch%3D%26rsv_enter%3D1%26inputT%3D3712; "
                                   "sessid=07475D2A-2B7F-AB74-9AA7-D2A0A0C9405B; als=0; "
                                   "lp_lt_ut=6117644281897975bfb831788e688228; "
                                   "ajk_member_captcha=18e942dc45afd9f788d4802593f9fae6; ctid=17; isp=true; "
                                   "Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1526803037; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1526803346; __xsptplusUT_8=1; _gat=1;"
                                   " __xsptplus8=8.2.1526802941.1526805099.14%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%236CuavhY4MOpRuaHFmbyj9N7jDwOnoRLH%23; _"
                                   "ga=GA1.2.1600018811.1526800135; _gid=GA1.2.412546660.1526800135; aQQ_ajkgucom%2Fs%3Fwd%3D%25E5%25AE%2589%25E5%id=6293A1E9-F0DF-E29D-5EBC-1579C952C81F; twe=2; "
                                   "58tj_uuid=fca5993b-462b-4bae-a3f9-631c589797d6; new_session=0;"
                                   " init_refer=https%253A%252F%252Fbeijing.anjuke.com%252F%253Fpi%253DPZ-baidu-pc-all-biaoti; new_uv=2"
                          }
            # 利用更强大的 Request 类来构建一个请求
            req=urllib.request.Request(self.url,headers=page_headers)

            #获取返回的网页内容
            data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
            # 获取响应码
            code=urllib.request.urlopen(req).code
            # 需要打开的网址
            uri=urllib.request.urlopen(req).url
            print(code)
            print(uri)
            return code,uri,data
        except Exception as e:
            print(e)
            return 0,0,0


    def get_house(self):
        region = "延庆"
        # 用于存储去掉前后空白后的字符串
        house_door_models = []
        house_contact_names = []
        house_addr = []
        house_detail_addr = []
        # 调用get_data()方法
        code,uri,data=self.get_data()
        # 创建数据库连接对象
        conn = ConnectDb('127.0.0.1', 3306, 'root', '', 'house', 'utf8')

        # 响应码为200代表响应成功
        if uri!="https://bj.zu.anjuke.com/fangyuan/yanqing/" and code==200:
            # 解析html字符串
            html=etree.HTML(data)

            # Xpath获取静态文本 ，根据标签爬取要爬去信息内容
            house_title=html.xpath('//div[@class="zu-info"]/h3/a/@title')
            print(house_title)
            print(len(house_title))

            house_url=html.xpath('//div[@class="zu-info"]/h3/a/@href')
            print(house_url)
            print(len(house_url))

            house_door_model=html.xpath('//div[@class="zu-info"]/p[@class="details-item tag"][1]/text()[1]')
            for i in house_door_model:
                result = i.strip()
                house_door_models.append(result)
            print(house_door_models)
            print(len(house_door_models))

            house_area=html.xpath('//div[@class="zu-info"]/p[@class="details-item tag"][1]/text()[2]')
            print(house_area)
            print(len(house_area))

            house_floor=html.xpath('//div[@class="zu-info"]/p[@class="details-item tag"][1]/text()[3]')
            print(house_floor)
            print(len(house_floor))

            house_contact_name=html.xpath('//div[@class="zu-info"]/p[@class="details-item tag"][1]/text()[4]') #姓名
            for i in house_contact_name:
                result = i.strip()
                house_contact_names.append(result)
            print(house_contact_names)
            print(len(house_contact_names))

            house_name=html.xpath('//div[@class="zu-info"]/address[@class="details-item"]/a/text()')
            print(house_name)
            print(len(house_name))

            house_address=html.xpath('//div[@class="zu-info"]/address[@class="details-item"]/text()[2]')
            # 去除字符串左右的空格再存入列表中
            for i in house_address:
                result = i.strip()
                house_addr.append(result)
            print(house_address)
            print(len(house_address))
            # # 连接两个列表中的元素
            for i in range(len(house_name)):
                house_detail_addr.append(house_addr[i]+" "+house_name[i])
            print(house_detail_addr)
            print(len(house_detail_addr))

            house_rent_type=html.xpath('//div[@class="zu-info"]/p[@class="details-item bot-tag clearfix"]/span[@class="cls-1"]/text()')
            print(house_rent_type)
            print(len(house_rent_type))

            house_orientation=html.xpath('//div[@class="zu-info"]/p[@class="details-item bot-tag clearfix"]/span[@class="cls-2"]/text()')
            print(house_orientation)
            print(len(house_orientation))

            # house_near_subway=html.xpath('//div[@class="zu-info"]/p[@class="details-item bot-tag clearfix"]/span[@class="cls-3"]/text()')
            # print(house_near_subway)
            # print(len(house_near_subway))

            house_price=html.xpath('//div[@class="zu-side"]/p[1]/strong/text()')
            for i in range(len(house_price)):
                house_price[i] += "元/月"
            print(house_price)
            print(len(house_price))

            house_image = html.xpath('//a[@class="img"]/img[@class="thumbnail"]/@src')
            print(house_image)
            print(len(house_image))


            for i in range(len(house_title)):
                ajk_id = str(uuid.uuid1())
                sql = 'insert into ajk_renting_info ' \
                      'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                param = (ajk_id, region, house_title[i], house_url[i], house_door_models[i],
                         house_area[i], house_floor[i], house_contact_names[i], house_detail_addr[i],
                         house_rent_type[i], house_orientation[i], house_price[i], house_image[i])
                conn.insert_into_db(sql, param)
            # conn.close_connect()

        return uri


if __name__ == '__main__':
    try:
        url_start="https://bj.zu.anjuke.com/fangyuan/yanqing/"
        i = 1  # 记录访问的页数
        house = AnJuKe(url_start)
        uri = house.get_house()
        while uri != 'https://bj.zu.anjuke.com/fangyuan/':
            print("第"+str(i)+"页爬取完成")
            i += 1
            if i == 6:
                break
            print("正在爬取第"+str(i)+"页...")
            url = url_start+"p"+str(i)+"/"
            house = AnJuKe(url)
            uri = house.get_house()

    except Exception as e:
        print(str(e))














