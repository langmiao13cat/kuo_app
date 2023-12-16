# C:\Users\jerem\Desktop\addcat\liff_app\app.py
from flask import Flask, request, redirect, url_for, session, render_template
from app import send_to_line_bot  # 引入 LINE BOT 處理函數

app = Flask(__name__)
app.secret_key = '106-818-738'  # 設定一個秘密鑰匙用於保護 session 數據

products = [
    # 產品列表，每個產品是一個字典
    {
        'product_id': 'product_id1',
        'name': '原味香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 180,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/LJqO17X.jpg'
    },
    {
        'product_id': 'product_id2',
        'name': '原味香腸',
        'description': '小包裝(5條)-約330公克',
        'price': 100,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/cYFv5dR.jpg'
    },
    {
        'product_id': 'product_id3',
        'name': '蒜苗香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 180,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/prBzJEo.jpg'
    },
    {
        'product_id': 'product_id4',
        'name': '蒜苗香腸',
        'description': '小包裝(5條)-約330公克',
        'price': 100,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/JCNayqC.jpg'
    },
    {
        'product_id': 'product_id5',
        'name': '黑胡椒香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 180,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/YbKMOQn.jpg'
    },
    {
        'product_id': 'product_id6',
        'name': '黑胡椒香腸',
        'description': '小包裝(5條)-約330公克',
        'price': 100,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/0GyREhA.jpg'
    },
    {
        'product_id': 'product_id7',
        'name': '九層香腸塔',
        'description': '大包裝(9條)-約600公克',
        'price': 200,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/AjpjRyF.jpg'
    },
    {
        'product_id': 'product_id8',
        'name': '九層香腸塔',
        'description': '小包裝(5條)-約325公克',
        'price': 110,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/jLn3ETM.jpg'
    },
    {
        'product_id': 'product_id9',
        'name': '麻辣香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 220,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/CAk9gx3.jpg'
    },
    {
        'product_id': 'product_id10',
        'name': '麻辣香腸',
        'description': '小包裝(5條)-約325公克',
        'price': 120,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/kPnxpdJ.jpg'
    },
    {
        'product_id': 'product_id11',
        'name': '馬告香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 200,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/Oiyqo4e.jpg'
    },
    {
        'product_id': 'product_id12',
        'name': '馬告香腸',
        'description': '小包裝(5條)-約325公克',
        'price': 110,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/gqe03ee.jpg'
    },
    {
        'product_id': 'product_id13',
        'name': '五香高粱香腸',
        'description': '大包裝(9條)-約600公克',
        'price': 250,
        'category': '郭家香腸系列大包裝',
        'img_url': 'https://i.imgur.com/YqYDNvv.jpg'
    },
    {
        'product_id': 'product_id14',
        'name': '五香高粱香腸',
        'description': '小包裝(5條)-約330公克',
        'price': 140,
        'category': '郭家香腸系列小包裝',
        'img_url': 'https://i.imgur.com/7ZDZdaP.jpg'
    },
    {
        'product_id': 'product_id15',
        'name': '鹹豬肉',
        'description': '一條300克',
        'price': 150,
        'category': '郭家家常菜系列',
        'img_url': 'https://i.imgur.com/Pdl8UQT.jpg'
    },
    {
        'product_id': 'product_id16',
        'name': '郭家香腸禮盒-\n兩種口味組',
        'description': '兩種口味組(一盒約1200g)\n兩種口味郭家香腸組合，\n香腸口味最後備註，\n九層塔、五香、麻辣、馬告口味\n如果選擇以上四種補差價',
        'price': 400,
        'category': '郭家禮盒系列',
        'img_url': 'https://i.imgur.com/DFP8k4w.jpg'
    },
    {
        'product_id': 'product_id17',
        'name': '郭家香腸禮盒-\n三種口味組',
        'description': '三種口味組(一盒約1800g)\n三種口味郭家香腸組合，\n香腸口味最後備註，\n九層塔、五香、麻辣、馬告口味\n如果選擇以上四種補差價',
        'price': 580,
        'category': '郭家禮盒系列',
        'img_url': 'https://i.imgur.com/9tRljLi.jpg'
    },
    {
        'product_id': 'product_id18',
        'name': '郭家香腸禮盒-\n四種口味組',
        'description': '四種口味組(一盒約2400g)\n四種口味郭家香腸組合，\n香腸口味最後備註，\n九層塔、五香、麻辣、馬告口味\n如果選擇以上四種補差價',
        'price': 760,
        'category': '郭家禮盒系列',
        'img_url': 'https://i.imgur.com/NXODbar.jpg'
    },
    {
        'product_id': 'product_id19',
        'name': '郭家香腸禮盒-\n兩種口味組+一條鹹豬肉組',
        'description': '兩種口味組+一條鹹豬肉組(一盒約1200g)\n兩種香腸+一條鹹豬肉組合，\n香腸口味最後備註，\n九層塔、五香、麻辣、馬告口味\n如果選擇以上四種補差價',
        'price': 550,
        'category': '郭家禮盒系列',
        'img_url': 'https://i.imgur.com/NW8OO2O.jpg'
    },
    {
        'product_id': 'product_id20',
        'name': '豬肉漢堡排',
        'description': '一片35元/80公克，1組=3片',
        'price': 100,
        'category': '郭家輕鬆料理系列',
        'img_url': 'https://i.imgur.com/rTsQNu5.jpg'
    },
    {
        'product_id': 'product_id21',
        'name': '梅花豬片',
        'description': '300g/一包100元',
        'price': 100,
        'category': '郭家輕鬆料理系列',
        'img_url': 'https://i.imgur.com/G1l5fQg.jpg'
    },
    {
        'product_id': 'product_id21',
        'name': '黑胡椒肉片',
        'description': '一包100元，約350公克10片',
        'price': 100,
        'category': '郭家家常菜系列',
        'img_url': 'https://i.imgur.com/1d7Bk6e.jpg'
    },
]


# 購物車類別
class ShoppingCart:
    def __init__(self):
        self.items = []  # Initialize an empty list of items

    def add_product(self, product, quantity=1):
        self.items.append((product, quantity))  # Add a product to the cart

    def total_price(self):
        return sum(item['price'] * quantity for item, quantity in self.items)  # Calculate total price

    def view_cart(self):
        # Generate cart summary with product details and total price
        if not self.items:
            return "購物車是空的"
        cart_contents = [f"{item} - 數量: {quantity}" for item, quantity in self.items]
        total_price = self.total_price()
        return "\n".join(cart_contents) + f"\n總金額: {total_price}元"

    def update_quantity(self, product_id, new_quantity):
        for i, (product, quantity) in enumerate(self.items):
            if product['product_id'] == product_id:
                self.items[i] = (product, max(new_quantity, 0))  # Update or remove the item
                return
        print(f"購物車中沒有ID為 {product_id} 的產品")

    def remove_product(self, product_id):
        self.items = [item for item in self.items if item[0]['product_id'] != product_id]  # Remove a product

    def clear(self):
        self.items.clear()  # Clear all items in the cart


cart = ShoppingCart()  # Create an instance of ShoppingCart


@app.route('/')
def index():
    return render_template('index.html', products=products)  # Render the index page with product list


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Add a product to the shopping cart
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    product = next((p for p in products if p['product_id'] == product_id), None)
    if product:
        cart.add_product(product, quantity)
    return redirect(url_for('view_cart'))


@app.route('/view_cart')
def view_cart():
    # 假設您的購物車資訊存儲在 session 中
    cart_items = session.get('cart_items', [])
    total_price = session.get('total_price', 0)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/update_cart/<product_id>', methods=['GET'])
def update_cart(product_id):
    # Update the quantity of a product in the cart
    new_quantity = int(request.args.get('quantity', 1))
    cart.update_quantity(product_id, new_quantity)
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart.remove_product(product_id)  # Remove a product from the cart
    return redirect(url_for('view_cart'))


@app.route('/submit_order', methods=['POST'])
def submit_order():
    order_params = {
        'name': request.form.get('name'),
        'contact': request.form.get('contact'),
        'delivery_method': request.form.get('delivery'),
        'address': request.form.get('address', ''),
        'store_name': request.form.get('storeName', ''),
        'market_pickup': request.form.get('marketPickup', '')
    }

    # 獲取購物車的內容
    cart_items = [{'name': item['name'], 'price': item['price'], 'quantity': quantity}
                  for item, quantity in cart.items]

    # 計算購物車的總價格
    total_price = cart.total_price()

    # 發送訂單資訊到 LINE BOT
    send_to_line_bot(order_params, cart_items, total_price)

    # 儲存訂單數據到 session
    session['order_params'] = order_params
    session['cart_items'] = cart_items
    session['total_price'] = total_price

    # 清空購物車
    cart.clear()

    # 可選的：提交訂單後清除收件人信息
    session.pop('order_params', None)

    return redirect(url_for('order_confirmation'))


@app.route('/order_confirmation')
def order_confirmation():
    order_params = session.get('order_params')
    cart_items = session.get('cart_items')  # 從 session 中獲取購物車項目
    total_price = session.get('total_price', 0)

    if not order_params:
        return redirect(url_for('index'))

    return render_template('order_confirmation.html', order_params=order_params, cart_items=cart_items,
                           total_price=total_price)


@app.route('/clear_cart')
def clear_cart():
    cart.clear()  # Clear the shopping cart
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

# ngrok http --domain=divine-lightly-salmon.ngrok-free.app 80
# pip freeze > requirements.txt - 將當前虛擬環境中的所有包列表保存到 requirements.txt
# pip install -r requirements.txt - 從 requirements.txt 文件中安裝所有依賴
