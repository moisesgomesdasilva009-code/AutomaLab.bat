import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/executar', methods=['POST'])
def executar_automacao():
    # Aponta diretamente para o arquivo que você já criou na pasta
    caminho_bat = os.path.join(os.getcwd(), "comandos_bat.bat")

    # Verifica se o arquivo realmente está na pasta antes de tentar executar
    if not os.path.exists(caminho_bat):
        return jsonify({
            "mensagem": "Erro na execução.",
            "log_detalhes": "O arquivo comandos_bat.bat não foi encontrado."
        }), 404

    # 4. Executa o .bat existente usando subprocess.run()
    try:
        resultado_execucao = subprocess.run(
            [caminho_bat], 
            capture_output=True, 
            text=True, 
            shell=True
        )
        
        # 5. Captura o código de retorno[cite: 1]
        codigo_retorno = resultado_execucao.returncode
        log_saida = resultado_execucao.stdout
        log_erro = resultado_execucao.stderr

        if codigo_retorno == 0:
            mensagem_final = "Script comandos_bat.bat executado com sucesso!"
            log_detalhe = log_saida
        else:
            mensagem_final = f"Erro na execução (Código {codigo_retorno})."
            log_detalhe = log_erro if log_erro else log_saida

        return jsonify({
            "mensagem": mensagem_final,
            "log_detalhes": log_detalhe
        }), 200

    except Exception as e:
        return jsonify({
            "mensagem": "Falha crítica ao tentar executar o subprocesso.",
            "log_detalhes": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)