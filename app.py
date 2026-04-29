from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# =========================
# ROTAS HTML
# =========================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perfil.html")
def perfil():
    return render_template("perfil.html")

@app.route("/graficos.html")
def graficos():
    return render_template("graficos.html")

@app.route("/relatorios.html")
def relatorios():
    return render_template("relatorios.html")

# =========================
# API
# =========================

@app.route("/api/deputados")
def deputados():
    try:
        r = requests.get(
            "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome"
        )
        return jsonify(r.json())
    except:
        return jsonify({"erro": "falha ao buscar dados"}), 500

# =========================
# START
# =========================

if __name__ == "__main__":
    app.run(debug=True)
