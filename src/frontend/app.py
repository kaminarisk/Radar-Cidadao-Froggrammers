from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/deputados.html")
def deputados():
    return render_template("deputados.html")

@app.route("/perfil.html")
def perfil():
    return render_template("perfil.html")

@app.route("/relatorios.html")
def relatorios():
    return render_template("relatorios.html")

@app.route("/graficos.html")
def graficos():
    return render_template("graficos.html")


# 🔹 LISTA DE DEPUTADOS
@app.route("/api/deputados")
def api_deputados():
    r = requests.get(
        "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome"
    )
    return jsonify(r.json())


# 🔥 DADOS DO DEPUTADO (FOTO + PARTIDO + UF)
@app.route("/api/deputado/<int:id_dep>")
def deputado_info(id_dep):
    try:
        r = requests.get(
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_dep}"
        ).json()["dados"]

        return jsonify({
            "nome": r["nomeCivil"],
            "partido": r["ultimoStatus"]["siglaPartido"],
            "uf": r["ultimoStatus"]["siglaUf"],
            "foto": r["ultimoStatus"]["urlFoto"]
        })
    except:
        return jsonify({
            "nome": "Erro",
            "partido": "-",
            "uf": "-",
            "foto": ""
        })


# 🔥 GASTOS DO DEPUTADO
@app.route("/api/gastos/<int:id_dep>")
def gastos(id_dep):
    try:
        r = requests.get(
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_dep}/despesas?itens=100"
        ).json()

        return jsonify(r["dados"])
    except:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
