from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'tajne_heslo'

USERNAME = 'admin'
PASSWORD = 'heslo123'

@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect(url_for("chat"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        meno = request.form["username"]
        heslo = request.form["password"]
        if meno == USERNAME and heslo == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Zlé meno alebo heslo.")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/chat')
def chat():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/chat', methods=["POST"])
def chat_post():
    if not session.get("logged_in"):
        return jsonify({"response": "Neautorizovaný prístup"}), 401

    data = request.get_json()
    user_message = data.get("message", "")
    bot_response = simple_response(user_message)
    return jsonify({"response": bot_response})

def simple_response(msg):
    if not msg:
        return "Napíš mi niečo, prosím 🙂"

    msg = msg.lower()

    patterns = [
        (r"(ahoj|čau|nazdar|servus)", "Ahoj! Ako ti môžem pomôcť?"),
        (r"ako sa (máš|ti darí)", "Mám sa dobre, ďakujem za opýtanie! A ty?"),
        (r"(koľko je hodín|aktuálny čas)", f"Práve je {datetime.now().strftime('%H:%M:%S')}"),
        (r"čo je flask", "Flask je mikro webový framework pre Python. Umožňuje rýchle vytváranie webových aplikácií."),
        (r"čo je python", "Python je univerzálny programovací jazyk, známy svojou čitateľnosťou a jednoduchosťou."),
        (r"čo je html", "HTML je značkovací jazyk používaný na tvorbu webových stránok."),
        (r"čo je css", "CSS sa používa na štýlovanie HTML elementov – napríklad farby, rozloženie a písmo."),
        (r"čo je java", "Java je objektovo orientovaný programovací jazyk. Je vyvíjaný spoločnosťou Oracle. Jeho syntax vychádza z jazykov C a C++"),
        (r"(kto si|kto ťa vytvoril)", "Som jednoduchý chatbot, ktorý ti rád pomôže! 🙂"),
        (r"pomôž (mi|nám|s niečím)", "Samozrejme! Spýtaj sa ma, s čím konkrétne potrebuješ pomôcť."),
        (r"(povedz mi niečo o firme)", "Deutsche Telekom je jedna z najväčších telekomunikačných spoločností na svete so sídlom v Bonne, Nemecko. Deutsche Telekom IT Solutions Slovakia bola založená v roku 2006 v Košiciach. Počiatočný plán počítal s vytvorením centra podporných služieb pre rôzne informačné technológie - počnúc operačnými systémami, cez ERP systémy až po špecializované zákaznícke aplikácie. Drvivú časť našej činnosti je dnes možné zaradiť do kategórie spravovania a administrácie IKT."),
        (r"(zbohom|maj sa|čauko)", "Zbohom! Ak budeš niečo potrebovať, som tu. 👋"),
        (r"kontakt", "Ak potrebuješ kontakt, napíš nám e-mail na podpora@example.com."),
        (r"(daj mi nejaký vtip|napíš mi vtip|rozvesel ma)", "Prečo programátori milujú tmavý režim? Lebo svetlo priťahuje bugy. 😄"),
        (r"(prihlásenie|zabudol som heslo|problém s loginom)", "Použi prihlasovacie meno a heslo. Ak si ich zabudol, kontaktuj administrátora.")
    ]

    for pattern, response in patterns:
        if re.search(pattern, msg):
            return response

    return "Prepáč, nerozumiem tvojej otázke. Skús to povedať inak. 🤔"

if __name__ == '__main__':
    app.run(debug=True)
