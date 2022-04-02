from flask import Flask, render_template, request
from feistel import *

app = Flask("__main__")


@app.route('/', methods=['GET', 'POST'])
def crypto():
    if request.method == "POST":
        encrypted = request.form["encrypt"]
        key = request.form["key"]
        decrypted = request.form["decrypt"]
        if encrypted != '' and key != '':
            encrypted = encrypt(encrypted, key)
            return render_template("index.html", encrypted=encrypted)
        if decrypted != '' and key != '':
            decrypted = decrypt(decrypted, key)
            return render_template("index.html", decrypted=decrypted)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
