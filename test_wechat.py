# coding:utf-8
import requests

# # 微信公众号的Token
# TOKEN = 'chihao079685'
# EncodingASE = 'H8Y5ZWvoH4QpIf55GSL2jXsNkbpAf5AOopMSRTISpmu'

APPID = 'wx87ddf185b314a690'
APPSECRET = '91c3b1cb6614ae8dcbaf2950f3d9e52b'
# 获取access_token的URL
TOKEN_URL = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'


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


# 主函数
def main():
    access_token = get_access_token()
    if access_token:
        print(f"Access Token: {access_token}")
    else:
        print("Failed to get access token")


if __name__ == '__main__':
    main()

