import requests


def get_wechat_access_token(appid: str, secret: str) -> dict:
    """
    获取微信API访问令牌

    参数:
    - appid (str): 微信公众号的AppID
    - secret (str): 微信公众号的AppSecret

    返回:
    - dict: 包含访问令牌及相关信息的字典
    """
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error_code": response.status_code,
            "error_message": response.text
        }


def get_weixin_phone_number(access_token: str, code: str) -> dict:
    url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
    json_data = {"code": code}

    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error_code": response.status_code,
            "error_message": response.text
        }
