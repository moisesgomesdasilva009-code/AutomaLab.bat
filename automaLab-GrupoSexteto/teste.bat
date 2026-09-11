@echo off

echo ==============================
echo   AUTOMA LAB - TESTE
echo ==============================

echo.
echo Passo 1 - Criando uma pasta...
mkdir Teste

echo.
echo Passo 2 - Verificando se a pasta existe...

if exist Teste (
    echo A pasta Teste foi criada com sucesso.
) else (
    echo ERRO: A pasta Teste nao foi criada.
)

echo.
echo Passo 3 - Listando arquivos da pasta...

for %%A in (*) do (
    echo Arquivo encontrado: %%A
)

echo.
echo Processo finalizado.
pause
