# coding:utf-8
import requests

# 微信公众号的AppID和AppSecret
APPID = 'wx87ddf185b314a690'
APPSECRET = '91c3b1cb6614ae8dcbaf2950f3d9e52b'

# 获取access_token的URL
TOKEN_URL = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'

# 获取关注者列表的URL
FOLLOWERS_URL = 'https://api.weixin.qq.com/cgi-bin/user/get'


def get_access_token():
    try:
        # 发送GET请求获取access_token
        response = requests.get(TOKEN_URL)

        # 检查请求是否成功
        if response.status_code == 200:
            result = response.json()
            if 'access_token' in result:
                return result['access_token']
            else:
                print(f"Error: {result.get('errmsg', 'Unknown error')}")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_followers(access_token, next_openid=''):
    try:
        # 构建请求URL
        url = f'{FOLLOWERS_URL}?access_token={access_token}&next_openid={next_openid}'

        # 发送GET请求获取关注者列表
        response = requests.get(url)
        print('response', response)

        # 检查请求是否成功
        if response.status_code == 200:
            result = response.json()
            print('result', result)
            if 'data' in result:
                return result['data']['openid'], result.get('next_openid', '')
            else:
                print(f"Error: {result.get('errmsg', 'Unknown error')}")
                return [], ''
        else:
            print(f"Request failed with status code {response.status_code}")
            return [], ''
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], ''


# 主函数
def main():
    access_token = get_access_token()
    print('access_token', access_token)
    if access_token:
        next_openid = ''
        while True:
            openids, next_openid = get_followers(access_token, next_openid)
            if openids:
                print(f"OpenIDs: {openids}")
            if not next_openid:
                break
    else:
        print("Failed to get access token")


if __name__ == '__main__':
    main()
