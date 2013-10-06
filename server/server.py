from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/product/")
def product_price():
    return render_template('product.html')

@app.route("/generic/")
def generics():
    return "Generics with price"

if __name__ == "__main__":
    app.run(debug=True)
