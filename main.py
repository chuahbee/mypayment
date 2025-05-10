from flask import Flask, render_template, request, redirect, session, url_for
from admin.routes import admin_bp
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.register_blueprint(
    admin_bp, 
    url_prefix="/admin"
    )


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")






@app.route("/api_document_p2p")
def api_document_p2p():
    return render_template("api_document_p2p.html")

@app.route("/api_document_creditcard")
def api_document_creditcard():
    return render_template("api_document_creditcard.html")

@app.route("/api_document_bitfinex")
def api_document_bitfinex():
    return render_template("api_document_bitfinex.html")

@app.route("/api_document_awesomepay")
def api_document_awesomepay():
    return render_template("api_document_awesomepay.html")


if __name__ == "__main__":
    app.run(debug=True)
