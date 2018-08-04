# coding: utf-8
from __future__ import print_function
import sys, time
from xml.sax.saxutils import escape
import uuid
import datetime


FORMAT_TIME = '2017-03-16 18:22:06'

TIMESTAMP = int(time.time())  # 当前时间戳


class Item(object):

    def __init__(self, title, subtitle='', icon='icon.png'):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

    # def title(self):
    #     return self.title
    #
    # def subtitle(self):
    #     return self.subtitle
    #
    # def icon(self):
    #     return self.icon


def show_alfred_item_list(item_list):
    print('<items>')
    for item in item_list:
        arg = item.title
        uid = 'com.github.letiantian.timestamp-workflow-' + uuid.uuid4().__str__()
        title = item.title
        subtitle = item.subtitle
        icon = item.icon

        print('''
            <item arg="{}" uid="{}"><title>{}</title><subtitle>{}</subtitle><icon>{}</icon></item>
        '''.format(escape(arg), escape(uid), escape(title), escape(subtitle), escape(icon)))

    print('</items>')


def alfred_process():
    global TIMESTAMP
    TIMESTAMP = int(time.time())
    if len(sys.argv) == 3:
        input_str = sys.argv[2].strip()
        if input_str in ['', ' ', 'n', 'now']:
            pass
        else:
            try:
                ts = time.strptime(input_str, "%Y-%m-%d %H:%M:%S")
                TIMESTAMP = time.mktime(ts)
            except Exception as e:
                TIMESTAMP = int(input_str)

    values = [str(TIMESTAMP),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y-%m-%d %H:%M:%S'),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y/%m/%d %H:%M:%S'),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y-%m-%d'),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%H:%M:%S'),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y年%m月%d日'),
              datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y年%m月%d日 %H时%M分%S秒'),
              ]
    item_list = []
    for val in values:
        item_list.append(Item(title=val))

    show_alfred_item_list(item_list)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '--alfred':
        try:
            alfred_process()
        except Exception as ex:
            item_list = [Item(title=ex.__str__())]
            show_alfred_item_list(item_list)
    else:
        pass
        # todo. 命令行，支持多个参数


if __name__ == '__main__':

    main()
