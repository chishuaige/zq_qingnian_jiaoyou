# coding:utf-8
import sqlite3
import random
from datetime import datetime, timedelta


def create_table():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 删除表

    try:
        cursor.execute('''
                    DROP TABLE user_test1011;
                    ''')
    except:
        pass
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_test1011 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_id TEXT,
            input_xm TEXT,
            input_gh TEXT,
            input_wechat TEXT,
            input_csrq TEXT,
            input_jg TEXT,
            input_sex TEXT,
            input_sg TEXT,
            input_xg TEXT,
            input_xq TEXT,
            last_message_time TEXT)''')
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()
    print('create done')


# 增加
def sqlite_insert(insert_line):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 先查找之前的
    input_id = insert_line[0]
    select_line = f'SELECT * FROM user_test1011 where input_id="{input_id}"'
    rows = sqlite_select(select_line)
    if rows:
        sqlite_delete(input_id)

    # 插入数据
    cursor.execute(
        'INSERT INTO user_test1011 (input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', insert_line)
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()
    print('insert done')


def sqlite_select(select_line):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询数据
    # select_line = 'SELECT * FROM user_info where input_id=xxx'    # demo
    cursor.execute(select_line)
    rows = cursor.fetchall()

    # 关闭连接
    conn.close()
    return rows


def sqlite_select_total(input_id):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询数据
    # select_line = 'SELECT * FROM user_info where input_id=xxx'    # demo
    sqlite_select_total = f'SELECT * FROM user_test1011 where input_id="{input_id}"'
    cursor.execute(sqlite_select_total)
    row = cursor.fetchall()
    if row:
        row = row[0]
    # 关闭连接
    conn.close()
    return row


def sqlite_delete(input_id):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    try:
        # 执行删除语句
        delete_line = f"DELETE FROM user_test1011 WHERE input_id = '{input_id}'"
        cursor.execute(delete_line)
        # 提交事务
        conn.commit()
        print("delete done")
    finally:
        # 关闭数据库连接
        conn.close()


# 多条件用匹配
def sqlite_macth(select_line):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询数据
    # select_line = 'SELECT * FROM user_info where input_id=xxx'    # demo
    cursor.execute(select_line)
    rows = cursor.fetchall()

    # 关闭连接
    conn.close()
    if not rows:
        content = '没有匹配到合适的朋友哦'
        return content
    else:
        # TODO 目前是随机匹配一个，待补充推荐逻辑
        row = random.choice(rows)

    return row


def check_last_message_time(input_id):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('mydatabase.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 检查用户是否存在
    cursor.execute('SELECT last_message_time FROM user_test1011 WHERE input_id = ?', (input_id,))
    row = cursor.fetchone()
    if row[-1] == None:
        # 更新或插入用户记录
        current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('UPDATE user_test1011 SET last_message_time = ? WHERE input_id = ?', (current_time_str, input_id))
        conn.commit()
        check_res = True
    else:
        last_message_time = datetime.strptime(row[-1], '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()
        # 检查是否超过24小时
        if current_time - last_message_time < timedelta(hours=24):
            check_res = False

        else:
            # 更新或插入用户记录
            current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('UPDATE user_test1011 SET last_message_time = ? WHERE input_id = ?', (current_time_str, input_id))
            conn.commit()
            check_res = True
    # 关闭连接
    conn.close()
    return check_res


if __name__ == '__main__':
    # pass
    # create_table()
    #
    # exit()

    # # # # ================================================增加================================================
    # input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq = \
    #     "liu", "刘亦菲", "079685", "13475978870", "19920412", "liaoning", "女", "175cm以上", "I", "美食、钓鱼"
    # #
    # insert_line = (
    # input_id, input_xm, input_gh, input_wechat, input_csrq, input_jg, input_sex, input_sg, input_xg, input_xq)  # demo_data
    # sqlite_insert(insert_line)
    # # #
    # ================================================查找================================================

    # select_line = 'SELECT * FROM user_test1011 where input_sex="男"'
    select_line = 'SELECT * FROM user_test1011'
    rows = sqlite_select(select_line)
    print(rows)

    #
    # # # 查找全部
    # # input_id = 'chi'
    # # row_out = sqlite_select_total(input_id)
    # # print(row_out)
    # # #
    # # # # # ================================================删除================================================
    # # # # input_id = 'abc'
    # # # # sqlite_delete(input_id)
    #
    # #================================================检查================================================
    input_id = 'liu'
    check_res = check_last_message_time(input_id)
    print('check_res', check_res)