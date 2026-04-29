import os
import requests
from flask import Flask, jsonify, render_template

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "src/frontend/templates"),
    static_folder=os.path.join(base_dir, "src/frontend/static"),
    static_url_path="/static"
)

# =========================
# ROTAS HTML
# =========================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deputados.html")
def deputados_page():
    return render_template("deputados.html")

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
            "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome",
            timeout=10
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# =========================
# START
# =========================

if __name__ == "__main__":
    app.run(debug=True)
