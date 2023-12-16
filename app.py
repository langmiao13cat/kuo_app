# app.py
from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, \
    ButtonsTemplate, URIAction

app = Flask(__name__, template_folder='templates')

# 替換為您的 LINE Bot 金鑰
line_bot_api = LineBotApi(
    'HppsBdCGmoYL4Ly8icq84tloOJsy8VAsI/ntSmwbMyvkHRAtXeRjgdwrsrlI2v3BWp+M7jgNlRzcuA6DP098jrxMFFUSK09UxGopiQIBohXZ1CHR5WvN9jIDmtfSNjUwe7EPfwNuFTx57g9DoxenAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a2775000b7c42954ac4301a439d19491')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理 Follow 事件
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """我們是一家有著50年歷史的肉舖，
專注於提供優質的豬肉產品。

我們以傳統手工和創新研發為基礎，
致力於獨特口感的香腸系列，
讓您品味豐富的味蕾體驗。

我們引以為傲的是七種口味的香腸，
每一款都有令人驚艷的風味和口感。
選用優質的瘦肉前腿肉（胛心肉），
確保香腸Q彈、軟嫩多汁。

我們郭家肉舖，追求高品質產品，
為您帶來美味的食品體驗。

歡迎您加入郭家肉舖，
期待為您提供滿足味蕾的美味。"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg)
    )


# 定義處理 LINE Bot 訊息事件的處理函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    if message_text == '線上下訂':
        # 創建按鈕模板消息
        buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                title='請選擇您要的商品',
                text='點擊下面的按鈕來線上下訂',
                actions=[
                    URIAction(
                        label='來去逛逛',
                        uri='https://divine-lightly-salmon.ngrok-free.app'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message
        )
    else:
        app_url = 'https://divine-lightly-salmon.ngrok-free.app'
        response_message = f"請選擇您要的商品並加入到購物車: {app_url}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )


@handler.add(MessageEvent, message=TextMessage)
def send_to_line_bot(order_params, cart_items, total_price):
    message_content = f"訂單詳情: {order_params}，購物車: {cart_items}，總價: {total_price}"
    line_bot_api.push_message('用戶的 LINE ID', TextSendMessage(text=message_content))


# 啟動 Flask 應用程序，運行在 debug 模式下
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
