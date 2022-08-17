from flask import Flask,render_template,request
import os
import requests

app = Flask(__name__)

try:
    API_HOST = os.environ['API_HOST']
except:
    print("ERROR: Configure API_HOST as envirment variable ")
    exit()

@app.route('/')
def index():
    products = requests.get("%s/products" % API_HOST).json()
    return render_template('index.html',products=products)


# main driver function
if __name__ == '__main__':
    app.run(debug=True)
