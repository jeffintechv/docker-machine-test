from flask import Flask,render_template,request, jsonify
import os
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)

try:
    app.config['MYSQL_HOST'] = os.environ['DB_HOST']
    app.config['MYSQL_USER'] = os.environ['DB_USER']
    app.config['MYSQL_PASSWORD'] = os.environ['DB_PASSWORD']
    app.config['MYSQL_DB'] = os.environ['DB_NAME']
except:
    print("ERROR:Please Configure the following envirment variables to connect mysql")
    print("DB_HOST\nDB_USER\nDB_PASSWORD\nDB_NAME")
    exit()


mysql = MySQL(app)

def products_check():
    print("table checks")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SHOW TABLES LIKE 'products';")
    table = cursor.fetchone()
    if not table:
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE TABLE products (id MEDIUMINT NOT NULL AUTO_INCREMENT, name CHAR(50) NOT NULL,price CHAR(50) NOT NULL,stock CHAR(50) NOT NULL, PRIMARY KEY (id) );")
        mysql.connection.commit()
        cursor.executemany("""INSERT INTO products (name, price, stock)
                            VALUES (%s, %s, %s)""",
                            [
                                ("apple", 100, 25),
                                ("orange", 77, 123),
                                ("mango", 120, 20),
                                ("strawberry", 250, 89),
                            ])
        mysql.connection.commit()


@app.route('/')
def index():
    return "OK"

@app.route('/products')
def products():
    #check the product table is created, if not create table with values
    products_check()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from products;")
    products = list(cursor.fetchall())
    return jsonify(products)


# main driver function
if __name__ == '__main__':

    app.run(debug=True)
