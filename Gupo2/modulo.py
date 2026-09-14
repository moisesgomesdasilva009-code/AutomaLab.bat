import os
import subprocess
from datetime import datetime, timedelta

LOG_FILE = "faxineiro_log.txt"

def registrar_log(mensagem):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{agora}] {mensagem}\n")

def faxineiro_digital(pasta, extensoes, dias_limite=7):
    if not os.path.exists(pasta):
        registrar_log(f"ERRO: pasta '{pasta}' nao encontrada.")
        return False, "A pasta informada nao existe."

    agora = datetime.now()
    limite = agora - timedelta(days=dias_limite)
    arquivos = os.listdir(pasta)

    if not arquivos:
        registrar_log(f"AVISO: pasta '{pasta}' esta vazia.")
        return True, "Nenhum arquivo encontrado para limpar."

    total_removidos = 0
    for nome_arquivo in arquivos:
        caminho = os.path.join(pasta, nome_arquivo)
        if os.path.isfile(caminho):
            extensao = os.path.splitext(nome_arquivo)[1].lower().replace(".", "")
            if extensao in extensoes:
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho))
                if data_modificacao < limite:
                    os.remove(caminho)
                    total_removidos += 1

    registrar_log(f"SUCESSO: {total_removidos} arquivo(s) removido(s) em '{pasta}'.")
    return True, f"{total_removidos} arquivo(s) removido(s) com sucesso."

def gerar_bat(nome_grupo, pasta_alvo, extensoes):
    data_str = datetime.now().strftime("%Y%m%d")
    nome_arquivo = f"automalab_{nome_grupo}_{data_str}.bat"

    linhas = [
        "@echo off",
        f"echo Iniciando Faxineiro Digital - Grupo {nome_grupo}",
        f'IF NOT EXIST "{pasta_alvo}" (',
        f"    echo Pasta {pasta_alvo} nao encontrada.",
        "    exit /b 1",
        ")",
    ]

    for ext in extensoes:
        linhas.append(f'FOR %%F IN ("{pasta_alvo}\\*.{ext}") DO (')
        linhas.append("    echo Apagando %%F")
        linhas.append('    DEL "%%F"')
        linhas.append(")")

    linhas.append("echo Limpeza finalizada.")
    linhas.append("exit /b 0")

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    registrar_log(f"Arquivo .bat gerado: {nome_arquivo}")
    return nome_arquivo

def executar_bat(caminho_bat):
    resultado = subprocess.run([caminho_bat], shell=True)
    codigo = resultado.returncode
    if codigo == 0:
        registrar_log(f"Execucao de {caminho_bat} concluida com sucesso.")
    else:
        registrar_log(f"Execucao de {caminho_bat} falhou (codigo {codigo}).")
    return codigo

def executar_faxina_completa(pasta_alvo, extensoes, nome_grupo):
    try:
        sucesso_logica, mensagem = faxineiro_digital(pasta_alvo, extensoes)
        if not sucesso_logica:
            return False, mensagem

        bat_gerado = gerar_bat(nome_grupo, pasta_alvo, extensoes)
        codigo = executar_bat(bat_gerado)

        if codigo == 0:
            return True, mensagem
        else:
            return False, "Ocorreu um problema ao executar a limpeza. Verifique o log."

    except Exception as e:
        registrar_log(f"EXCECAO: {str(e)}")
        return False, "Erro inesperado. Consulte o arquivo de log."