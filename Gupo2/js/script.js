document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('automaForm');
    const logArea = document.getElementById('logArea');
    const btnExecutar = document.getElementById('btnExecutar');

    form.addEventListener('submit', async (event) => {
        // Previne o comportamento padrão de recarregar a página ao enviar o formulário
        event.preventDefault();

        // Captura os dados inseridos no formulário
        const task = document.getElementById('taskSelect').value;
        const directory = document.getElementById('dirInput').value;

        // Atualiza a interface visualmente
        btnExecutar.disabled = true;
        btnExecutar.textContent = "Executando...";
        logArea.style.color = "#fbbf24"; // Amarelo indicando processamento
        logArea.textContent = `Enviando requisição para o Python...\nTarefa: ${task}\nDiretório: ${directory}`;

        try {
            // Utilização do fetch() para enviar os dados ao backend em Python[cite: 1]
            // NOTA: O endereço 'http://localhost:5000/executar' assumirá que seu Flask está rodando nesta porta.
            const response = await fetch('http://localhost:5000/executar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tarefa: task,
                    diretorio: directory
                })
            });

            if (!response.ok) {
                throw new Error(`Erro na comunicação com o servidor: Status ${response.status}`);
            }

            // Captura o resultado real vindo do Python[cite: 1]
            const data = await response.json();
            
            // Mostra a resposta na área de log sem recarregar a página[cite: 1]
            logArea.style.color = "#4ade80"; // Verde indicando sucesso
            logArea.textContent = `[SUCESSO]\n${data.mensagem}\nLog: ${data.log_detalhes}`;

        } catch (error) {
            // Transformar erros em mensagens compreensíveis (conforme recomendado na Etapa 7)[cite: 1]
            logArea.style.color = "#f87171"; // Vermelho indicando erro
            logArea.textContent = `[ERRO DE COMUNICAÇÃO]\nNão foi possível conectar ao servidor Python.\nVerifique se o modulo.py (Flask) está rodando no terminal.\nDetalhe: ${error.message}`;
        } finally {
            // Restaura o estado do botão
            btnExecutar.disabled = false;
            btnExecutar.textContent = "Executar";
        }
    });
});