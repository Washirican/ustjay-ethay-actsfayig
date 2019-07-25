import os

import requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    fact = facts[0].getText()

    return fact.strip().rstrip('.')


@app.route('/')
def home():
    page = """
    <html>
    <head>
    <title> Pig Facts </title>
    <body>
    <h1>That'll do pig. That'll do.</h1>
    <p><b>Unnecessary Knowledge:</b>{}</p>
    <p><b>Piglatinized URL: </b>{} [<a href='{}' target="_blank">Link</a>]</p>
    </body>
    </html>
    """
    fact = get_fact()
    response = requests.post(
        'https://hidden-journey-62459.herokuapp.com/piglatinize/',
        data={'input_text': fact}
        )
    return page.format(
        fact,
        response.text.split('\n')[-4].strip(),
        response.url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
