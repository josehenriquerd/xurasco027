document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("churrasco-form");
    const tipoChurrasco = document.getElementById("tipo");

    // Quando o usuário selecionar "Churrasco Completo", marcar todas as carnes e acompanhamentos
    tipoChurrasco.addEventListener("change", function () {
        if (tipoChurrasco.value === "completo") {
            document.querySelectorAll('input[name="carne"]').forEach(el => el.checked = true);
            document.querySelectorAll('input[name="acompanhamento"]').forEach(el => el.checked = true);
        }
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const adultos = parseInt(document.getElementById("adultos").value) || 0;
        const criancas = parseInt(document.getElementById("criancas").value) || 0;
        const pagantes = parseInt(document.getElementById("pagantes").value) || adultos;
        const orcamento = parseFloat(document.getElementById("orcamento").value) || null;
        const tipo = tipoChurrasco.value;
        const modoFesta = document.getElementById("modo_festa").checked;

        // Corrigindo a captura das carnes e acompanhamentos
        const carnes = Array.from(document.querySelectorAll('input[name="carne"]:checked')).map(el => el.value);
        const acompanhamentos = Array.from(document.querySelectorAll('input[name="acompanhamento"]:checked')).map(el => el.value);

        if (!adultos || carnes.length === 0) {
            document.getElementById("resultado").innerHTML = '<p style="color: red;">Preencha adultos e pelo menos uma carne!</p>';
            return;
        }

        const btn = document.querySelector('button[type="submit"]');
        btn.disabled = true;

        fetch("http://127.0.0.1:5000/calcular", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ adultos, criancas, tipo, carnes, acompanhamentos, modo_festa: modoFesta, pagantes, orcamento })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const listaCompras = `
                <h3>Lista de Compras</h3>
                <strong>Carnes:</strong><br>${Object.entries(data.lista_compras.carnes).map(([k, v]) => ` - ${k}: ${v}`).join('<br>')}<br>
                <strong>Bebidas:</strong><br>
                - Cerveja: ${data.bebidas.cerveja_latas.toFixed(1)} latas<br>
                - Refrigerante: ${data.bebidas.refrigerante_litros.toFixed(1)} L<br>
                - Água: ${data.bebidas.agua_litros.toFixed(1)} L<br>
                <strong>Acompanhamentos:</strong><br>${Object.entries(data.acompanhamentos).map(([k, v]) => ` - ${k}: ${v.toFixed(2)} kg`).join('<br>') || ' - Nenhum selecionado'}<br>
                <strong>Carvão:</strong><br> - ${data.carvao_kg.toFixed(2)} kg
            `;

            const ajusteMsg = data.ajustado_orcamento ? `<p style="color: #ff5722;"><strong>Ajustado ao orçamento de R$ ${orcamento.toFixed(2)}!</strong></p>` : '';

            document.getElementById("resultado").innerHTML = `
                <h3>Resultado do Churrasco</h3>
                ${ajusteMsg}
                <p><strong>Carnes:</strong> ${data.total_carne_kg.toFixed(2)} kg (R$ ${data.preco_carne.toFixed(2)})</p>
                <p><strong>Bebidas:</strong> ${data.bebidas.cerveja_latas.toFixed(1)} latas de cerveja, ${data.bebidas.refrigerante_litros.toFixed(1)}L de refri, ${data.bebidas.agua_litros.toFixed(1)}L de água (R$ ${data.bebidas.preco_bebidas.toFixed(2)})</p>
                <p><strong>Acompanhamentos:</strong> ${Object.entries(data.acompanhamentos).map(([k, v]) => `${k}: ${v.toFixed(2)} kg`).join(', ') || 'Nenhum'} (R$ ${data.preco_acompanhamentos.toFixed(2)})</p>
                <p><strong>Carvão:</strong> ${data.carvao_kg.toFixed(2)} kg (R$ ${data.preco_carvao.toFixed(2)})</p>
                <p><strong>Tempo estimado:</strong> ${data.tempo_preparo} minutos</p>
                <p><strong>Preço Total:</strong> R$ ${data.preco_total.toFixed(2)}</p>
                <p><strong>Custo por Pessoa (entre ${pagantes} pagantes):</strong> R$ ${data.custo_por_pessoa.toFixed(2)}</p>
                ${listaCompras}
            `;
            document.getElementById("compartilharBtn").style.display = "block";
        })
        .catch(error => {
            document.getElementById("resultado").innerHTML = `<p style="color: red;">Erro: ${error.message}</p>`;
        })
        .finally(() => btn.disabled = false);
    });

    document.getElementById("compartilharBtn").addEventListener("click", function () {
        const resultado = document.getElementById("resultado").innerText;
        const blob = new Blob([resultado], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "Planejamento_Churrasco.txt";
        a.click();
        URL.revokeObjectURL(url);
    });
});
