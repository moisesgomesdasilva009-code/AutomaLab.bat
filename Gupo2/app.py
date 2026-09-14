from flask import Flask, request, jsonify, render_template
from modulo import executar_faxina_completa

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/executar", methods=["POST"])
def executar():
    dados = request.get_json()

    pasta_alvo = dados.get("pasta")
    extensoes = dados.get("extensoes", [])
    nome_grupo = dados.get("grupo", "grupo2")

    sucesso, mensagem = executar_faxina_completa(pasta_alvo, extensoes, nome_grupo)

    return jsonify({
        "sucesso": sucesso,
        "mensagem": mensagem
    })

if __name__ == "__main__":
    app.run(debug=True)