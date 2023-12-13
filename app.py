# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)


class Product:
    def __init__(self, product_id, name, description, price, category, img_url):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.img_url = img_url

    def __str__(self):
        return f"{self.name} - {self.description} - {self.price}元 - 圖片: {self.img_url}"


products_data = [
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

products = [Product(**product) for product in products_data]


# 路由到產品目錄頁面。
@app.route('/categories')
def categories_page():
    # 商品分類列表
    categories_list = [
        {'category': '郭家香腸系列大包裝', 'img_url': 'https://i.imgur.com/G6A2etj.png'},
        {'category': '郭家香腸系列小包裝', 'img_url': 'https://i.imgur.com/G6A2etj.png'},
        {'category': '郭家輕鬆料理系列', 'img_url': 'https://i.imgur.com/3khtKBo.png'},
        {'category': '郭家禮盒系列', 'img_url': 'https://i.imgur.com/RCWh92m.png'},
        {'category': '郭家家常菜系列', 'img_url': 'https://i.imgur.com/5EIPMQA.png'},
        {'category': '郭家市場肉品推薦', 'img_url': 'https://i.imgur.com/n3PaEOk.png'}
    ]
    return render_template('categories.html', categories=categories_list)


def categorize_products(products):
    categorized = {}
    for product in products:
        category = product.category
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(product)
    return categorized


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity=1):
        self.items.append((product, quantity))

    def total_price(self):
        return sum(item[0].price * item[1] for item in self.items)

    def view_cart(self):
        cart_contents = []
        total_price = 0
        for item, quantity in self.items:
            cart_contents.append(f"{item} - 數量: {quantity}")
            total_price += item.price * quantity
        cart_summary = "\n".join(cart_contents) + f"\n總金額: {total_price}元"
        return cart_summary if cart_contents else "購物車是空的"

    def update_quantity(self, product_name, new_quantity):
        for i, (item, quantity) in enumerate(self.items):
            if item.name == product_name:
                if new_quantity > 0:
                    self.items[i] = (item, new_quantity)
                else:
                    del self.items[i]
                return
        print(f"購物車中沒有名為 {product_name} 的產品")

    def remove_product(self, product_name):
        self.items = [item for item in self.items if item[0].name != product_name]

    def clear_cart(self):
        self.items.clear()


# 創建一個購物車實例
cart = ShoppingCart()

# 添加一些產品到購物車
cart.add_product(products[0], 2)
cart.add_product(products[2], 1)

# 查看購物車內容
cart_content = cart.view_cart()


@app.route('/')
def index():
    categorized_products = categorize_products(products)
    return render_template('index.html', categories=categorized_products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    # 查找產品
    product = next((p for p in products if p.product_id == product_id), None)
    if product:
        # 添加到購物車
        cart.add_product(product, quantity)
        return redirect(url_for('view_cart'))
    return redirect(url_for('index'))


@app.route('/cart')
def view_cart():
    # 傳遞購物車內容到模板
    return render_template('cart.html', cart_items=cart.items, total_price=cart.total_price())


@app.route('/update_cart/<product_id>', methods=['GET'])
def update_cart(product_id):
    new_quantity = int(request.args.get('quantity', 1))
    cart.update_quantity(product_id, new_quantity)
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart.remove_product(product_id)
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
    # 假設 cart 是購物車的實例
    cart_items = cart.items
    total_price = cart.total_price()
    return render_template('order_confirmation.html', order_params=order_params, cart_items=cart_items,
                           total_price=total_price)


@app.route('/order_confirmation')
def order_confirmation():
    # 顯示訂單確認的相關內容
    return render_template('order_confirmation.html')


if __name__ == '__main__':
    app.run(debug=True)
