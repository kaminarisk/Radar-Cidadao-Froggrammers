from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')


# 🔹 PÁGINAS
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


# 🔹 LISTA DE DEPUTADOS (PADRONIZADO)
@app.route("/api/deputados")
def api_deputados():
    try:
        r = requests.get(
            "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome"
        ).json()

        lista = []

        for d in r.get("dados", []):
            lista.append({
                "id": d.get("id"),
                "nome": d.get("nome"),
                "partido": d.get("siglaPartido"),
                "uf": d.get("siglaUf"),
                "foto": d.get("urlFoto")
            })

        return jsonify(lista)

    except:
        return jsonify([])


# 🔥 PERFIL DO DEPUTADO
@app.route("/api/deputado/<int:id_dep>")
def deputado_info(id_dep):
    try:
        r = requests.get(
            f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_dep}"
        ).json()["dados"]

        return jsonify({
            "nome": r.get("nomeCivil"),
            "partido": r.get("ultimoStatus", {}).get("siglaPartido"),
            "uf": r.get("ultimoStatus", {}).get("siglaUf"),
            "foto": r.get("ultimoStatus", {}).get("urlFoto")
        })

    except:
        return jsonify({
            "nome": "Erro",
            "partido": "-",
            "uf": "-",
            "foto": ""
        })


# 🔥 GASTOS COMPLETOS (2025 + 2026)
@app.route("/api/gastos/<int:id_dep>")
def gastos(id_dep):
    try:
        todos = []

        for ano in [2025, 2026]:
            pagina = 1

            while True:
                url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_dep}/despesas?ano={ano}&pagina={pagina}&itens=100"

                res = requests.get(url).json()
                dados = res.get("dados", [])

                if not dados:
                    break

                for g in dados:
                    todos.append({
                        "dataDocumento": g.get("dataDocumento"),
                        "tipoDespesa": g.get("tipoDespesa"),
                        "valorDocumento": g.get("valorDocumento", 0)
                    })

                pagina += 1

        # 🔥 ORDENA POR DATA (mais recente primeiro)
        todos.sort(
            key=lambda x: x["dataDocumento"] if x["dataDocumento"] else "",
            reverse=True
        )

        return jsonify(todos)

    except:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
