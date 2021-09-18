import requests
import time
import json
from lxml import etree


def get_response(url):
    while True:
        try:
            time.sleep(0.2)
            res_ = requests.get(url)
            return res_.text
        except requests.exceptions.SSLError:
            print("请求过于频繁被服务器拒绝\n", "30秒后重新尝试获取该页面商品信息：", url)
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    province = input("请输入要关注的省份，(例如：福建)")
    city = input("请输入对应省份内的城市，(例如：厦门)")
    # province = "福建"
    # city = "厦门"
    if province and city:
        province = province
        city = city
    else:
        province = "福建"
        city = "厦门"
    u = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city={}-{}".format(province,
                                                                                                            city)
    old_update_time = ""
    old_now_ = ""
    first = True
    t = 1
    print("{:-^110}".format("Data from Baidu, the fastest data update"))
    information = ['{: <10}'.format("厦门"), '{: <20}'.format("update-time"), '{: <10}'.format("现有确诊"),
                   '{: <10}'.format("新增本土"), '{: <10}'.format("新增无症状"), '{: <10}'.format("累计确诊"),
                   '{: <10}'.format("累计治愈"), '{: <10}'.format("累计死亡\t")]

    for c in information:
        if c != information[-1]:
            print(c, end="")
        else:
            print(c)
    while True:
        res = get_response(u)
        pa = etree.HTML(res)
        data = json.loads(pa.xpath("//script[contains(text(), 'cityCode')]/text()")[0])
        # data = pa.xpath("//script[contains(text(), 'cityCode')]/text()")[0]
        # print(data)

        new_update_time = data["component"][0]["mapLastUpdatedTime"]
        province_data = [i for i in data["component"][0]["caseList"] if i["area"] == province][0]
        # print(json.dumps(province_data))
        city_data = [i for i in province_data["subList"] if i["city"] == city][0]
        # print(json.dumps(city_data))
        now_ = city_data["curConfirm"]
        new = city_data["confirmedRelative"]
        new_normal = city_data["asymptomaticRelative"]
        all_ = city_data["confirmed"]
        history_cured = city_data["crued"]
        history_death = city_data["died"]

        # print(new_update_time)
        # print(now_)
        # print(new)
        # print(new_normal)
        # print(all_)
        # print(history_cured)
        # print(history_death)
        # t+=1

        if now_ != old_now_ or new_update_time != old_update_time:
        # if True:
        # if t > 3:
            if first:
                pass
            else:
                print("\r", end="")
            print('{: >22}\t'.format(new_update_time), end="")
            print('{: >15}\t'.format(now_), end="")
            print('{: >13}\t'.format(new), end="")
            print('{: >11}\t'.format(new_normal), end="")
            print('{: >12}\t'.format(all_), end="")
            print('{: >10}\t'.format(history_cured), end="")
            print('{: >10}\t'.format(history_death))
            print("\t ", end="")

            old_update_time = new_update_time
            old_now_ = now_
            # t+=1
        else:
            print("\r{:-^97}".format("120秒自动更新一次，当前更新时间：" + str(time.strftime("%Y.%m.%d %H:%M:%S"))), end="")
            first = False
            # t+=1

        time.sleep(120)
        # print("\r", end="")
