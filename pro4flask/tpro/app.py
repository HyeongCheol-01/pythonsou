from flask import Flask, render_template, session, jsonify

app = Flask(__name__)
app.secret_key = 'shop_secret_key'

products = {
    1: {"name": "최강 가성비 노트북", "price": 890000},
    2: {"name": "프리미엄 무선 이어폰", "price": 150000},
    3: {"name": "4K 울트라 모니터", "price": 320000}
}

@app.route('/')
def index():
    # 전체 수량 합계 계산
    cart = session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    p_id = str(product_id) # 세션 키는 문자열로 저장됨

    if p_id in cart:
        cart[p_id]['quantity'] += 1
    else:
        if product_id in products:
            cart[p_id] = products[product_id].copy()
            cart[p_id]['quantity'] = 1
    
    session.modified = True
    total_count = sum(item['quantity'] for item in cart.values())
    return jsonify({"status": "success", "cart_count": total_count})

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    cart_count = sum(item['quantity'] for item in cart.values())
    return render_template('cart.html', items=cart, total=total, cart_count=cart_count)

@app.route('/remove_from_cart/<p_id>', methods=['POST'])
def remove_from_cart(p_id):
    cart = session.get('cart', {})
    if p_id in cart:
        del cart[p_id]
        session.modified = True
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    total_count = sum(item['quantity'] for item in cart.values())
    return jsonify({"status": "success", "cart_count": total_count, "total": total})