from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import time
import uuid
import json
import os
from function_operate_sqlite import sqlite_insert, sqlite_select, sqlite_select_total, sqlite_delete

app = Flask(__name__)


# ====================================填报表单 start====================================
@app.route('/<article_id>', methods=['POST', 'GET'])
def index_page(article_id):
    return render_template('index_填写资料.html')


@app.route('/index_提交成功', methods=['POST'])
def submit():
    url = request.url  # 获取当前请求的 URL
    referrer = request.referrer  # 获取来源页面的 URL
    print(f'url {url}')
    print(f'referrer {referrer}')
    # 获取数据
    form = request.form
    print(form)
    # 对应的字段分别是openid、姓名、工号、微信号、出生日期、籍贯、性别、身高、性格、兴趣
    input_id = referrer.rsplit('/', 1)[1]
    input_xm = form['inputxm']
    input_gh = form['inputgh']
    input_wechat = form['inputwechat']
    input_csrq = form['inputcsrq']
    input_jg = form['city']
    input_sex = form['sex']
    input_sg = form['inputsg']
    input_xg = form['inputxg']
    input_xq_t = ['美食', '钓鱼', '看剧', '游泳', '健身', '跳舞', '唱歌', '游戏', '篮球', '足球', '羽毛球', '其他']
    input_xq = '、'.join([i for i in input_xq_t if i in form])
    print('===========================================================================')
    print(input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq)
    # 存sqlite,字段依次是：openid、姓名、工号、微信号、出生日期、籍贯、性别、身高、性格、兴趣
    insert_line = (input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq)  # demo_data
    sqlite_insert(insert_line)
    return render_template('index_提交成功.html')
# ====================================填报表单 end ====================================


# ====================================查看表单 start====================================
# 自己查看自己的
@app.route('/show/<article_id>')
def index_view(article_id):
    # Python 3.7 及以后的版本中，标准的 dict 类型已经保证了插入顺序的稳定性
    # 查询数据
    input_id = article_id
    row_out = sqlite_select_total(input_id)
    # (1, 'abcd', '迟帅哥', '079685', '男', '19920412', '175cm以上', 'I', '13475978870', '羽毛球', 'abcd.png')
    # input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq
    print(row_out)
    row_out = row_out[1:]
    form_data_dict = {'姓名': row_out[1],
                      '工号': row_out[2],
                      '微信号': row_out[3],
                      '出生日期': row_out[4],
                      '籍贯': row_out[5],
                      '性别': row_out[6],
                      '身高': row_out[7],
                      '性格': row_out[8],
                      '兴趣': row_out[9]}

    return render_template('index_查看资料.html', form_data=form_data_dict)


# 别人查看你的
@app.route('/show_other/<article_id>')
def index_view_other(article_id):
    # Python 3.7 及以后的版本中，标准的 dict 类型已经保证了插入顺序的稳定性
    # 查询数据
    input_id = article_id
    row_out = sqlite_select_total(input_id)
    print(row_out)
    row_out = row_out[1:]
    form_data_dict = {'姓名': row_out[1],
                      '工号': row_out[2],
                      '微信号': row_out[3],
                      '出生日期': row_out[4],
                      '籍贯': row_out[5],
                      '性别': row_out[6],
                      '身高': row_out[7],
                      '性格': row_out[8],
                      '兴趣': row_out[9]}

    return render_template('index_查看资料other.html', form_data=form_data_dict)
# ====================================查看表单 end=========================================


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5054)

