from wxcloudrun import response


def get_wx_uid(request):
    weixin_openid = request.headers.get('x-wx-openid')

    return weixin_openid
