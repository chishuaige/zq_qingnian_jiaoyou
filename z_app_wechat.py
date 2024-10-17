# coding:utf-8
from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import hashlib
import time
import random
from function_operate_sqlite import sqlite_insert, sqlite_select, sqlite_select_total, sqlite_delete, check_last_message_time

app = Flask(__name__)

# 微信公众号的Token
TOKEN = 'chihao079685'
EncodingASE = 'H8Y5ZWvoH4QpIf55GSL2jXsNkbpAf5AOopMSRTISpmu'


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证服务器
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')

        # 根据微信的文档，这里需要进行签名验证
        token = TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list).encode('utf-8')
        if hashlib.sha1(tmp_str).hexdigest() == signature:
            return make_response(echostr)
        else:
            return make_response('')

    elif request.method == 'POST':
        print('=======================================================================')
        # 接收消息
        xml_data = request.data
        xml = ET.fromstring(xml_data)
        to_user_name = xml.find('ToUserName').text
        from_user_name = xml.find('FromUserName').text
        msg_type = xml.find('MsgType').text.lower()
        # 非正常逻辑：如果消息类型不是文字的
        if msg_type == 'event':
            # 没发消息，说明是新关注
            response_content = '终于等到你！想交友想恋爱，就在这！操作非常简单，就两步。\n' \
                      '第一步：填写资料 回复1\n' \
                      '第二步：匹配交友 回复2\n' \
                      '注：为保证用户体验，使用匹配交友功能后，必须等待24小时才能再次使用该功能。解锁更多功能回复0'
            # 构造回复消息
            response_xml = f"""
            <xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{int(time.time())}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{response_content}]]></Content>
            </xml>
            """
            return make_response(response_xml)

        # 发消息，分三种：填写资料/匹配心动/其他
        content = xml.find('Content').text
        # 填写资料
        if content == '1' or content == '填写资料':
            content = f'来吧，先把资料填好，http://124.221.238.156:5054/{from_user_name}'
        # 匹配交友
        elif content == '2' or content == '匹配交友':

                row = sqlite_select_total(from_user_name)
                if row:
                    # 检查是否超过24小时
                    check_res = check_last_message_time(from_user_name)
                    if check_res:

                        # sex_self = row['input_sex']
                        # if sex_self == '男':
                        #     sex_other = '女'
                        # else:
                        #     sex_other = '男'
                        # select_line = f'SELECT * FROM user_test1011 where input_sex="{sex_other}"'
                        # rows = sqlite_select(select_line)
                        # row = random.choice(rows)
                        # row_gh, row_wechat = row['input_gh'], row['input_wechat']
                        # content = f'哇，匹配到了有缘人\n对方的工号: {row_gh}，对方的微信号: {row_wechat}'
                        content = f'哇，匹配到了有缘人\n对方的工号:12345 ，对方的微信号: 12345'
                    else:
                        content = '距离上次匹配还不到24小时哦'
                else:
                    content = f'先把资料填好才能匹配交友哦，http://124.221.238.156:5054/{from_user_name}'

        elif content == '查看资料' or content == '3':
            content = f'okk，看吧看吧，http://124.221.238.156:5054/show/{from_user_name}'
        elif content == '删除资料' or content == '4':
            content = f'okk，资料已删除'
            sqlite_delete(from_user_name)
        elif content == '0':
            content = '已开发功能如下：\n' \
                      '填写资料 回复1\n' \
                      '匹配交友 回复2\n' \
                      '查看资料 回复3\n' \
                      '删除资料 回复4\n'

        else:
            content = '其他关键词待开发哦'

        # 正常逻辑
        # try:
        #     # 发消息，分三种：填写资料/匹配心动/其他
        #     content = xml.find('Content').text
        #     # 填写资料
        #     if content == '1':
        #         content = f'来吧，先把资料填好，http://124.221.238.156:5054/{from_user_name}'
        #     # 匹配交友
        #     elif content == '2':
        #
        #             row = sqlite_select_total(from_user_name)
        #             if row:
        #                 # 检查是否超过24小时
        #                 check_res = check_last_message_time(from_user_name)
        #                 if check_res:
        #
        #                     # sex_self = row['input_sex']
        #                     # if sex_self == '男':
        #                     #     sex_other = '女'
        #                     # else:
        #                     #     sex_other = '男'
        #                     # select_line = f'SELECT * FROM user_test1011 where input_sex="{sex_other}"'
        #                     # rows = sqlite_select(select_line)
        #                     # row = random.choice(rows)
        #                     # row_gh, row_wechat = row['input_gh'], row['input_wechat']
        #                     # content = f'哇，匹配到了有缘人\n对方的工号: {row_gh}，对方的微信号: {row_wechat}'
        #                     content = f'哇，匹配到了有缘人\n 对方的工号:12345 ，对方的微信号: 12345'
        #                 else:
        #                     content = '距离上次匹配还不到24小时哦'
        #             else:
        #                 content = f'先把资料填好才能匹配交友哦，http://124.221.238.156:5054/{from_user_name}'
        #     elif content == '查看资料':
        #         content = f'okk，看吧看吧，http://124.221.238.156:5054/show/{from_user_name}'
        #     elif content == '删除资料':
        #         content = f'okk，资料已删除'
        #         sqlite_delete(from_user_name)
        #     else:
        #         content = '其他关键词待开发哦'

        # except:
        #     # 其他类型
        #     content = '终于等到你！想交友想恋爱，就在这！操作非常简单，就两步。\n' \
        #               '第一步：填写资料 回复1\n' \
        #               '第二步：匹配交友 回复2\n' \
        #               '注：为保证用户体验，使用匹配交友功能后，必须等待24小时才能再次使用该功能。解锁更多功能回复3'

        # 处理消息
        response_content = f'{content}'

        # 构造回复消息
        response_xml = f"""
        <xml>
            <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
            <CreateTime>{int(time.time())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{response_content}]]></Content>
        </xml>
        """

        return make_response(response_xml)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)