let graficoProgresso = null;

function atualizarGrafico() {
  fetch("/api/estatisticas")
    .then(function (resposta) {
      if (!resposta.ok) throw new Error(resposta.statusText);
      return resposta.json();
    })
    .then(function (dados) {
      const canvas = document.getElementById("grafico-progresso");
      if (canvas) {
        if (graficoProgresso) graficoProgresso.destroy();
        graficoProgresso = new Chart(canvas, {
          type: "doughnut",
          data: {
            labels: ["Pendente", "Em andamento", "Concluída"],
            datasets: [{
              data: [dados.pendente, dados["em andamento"], dados.concluida],
              backgroundColor: ["#ffc107", "#0d6efd", "#198754"],
              borderWidth: 2,
            }],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: "bottom" },
            },
          },
        });
      }

      const contador = document.getElementById("contador-total");
      if (contador) {
        contador.textContent = `Total de ${dados.total} tarefa(s)`;
      }
    })
    .catch(function (erro) {
      console.error("Erro ao carregar estatísticas:", erro);
    });
}

document.addEventListener("DOMContentLoaded", atualizarGrafico);
document.addEventListener("tarefas-atualizadas", atualizarGrafico);