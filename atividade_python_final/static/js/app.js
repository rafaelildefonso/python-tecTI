const STATUS_INFO = {
  "pendente":    { rotulo: "Pendente",     classe: "status-pendente",     badge: "text-bg-warning" },
  "em andamento":{ rotulo: "Em andamento", classe: "status-em-andamento", badge: "text-bg-primary" },
  "concluida":   { rotulo: "Concluída",    classe: "status-concluida",    badge: "text-bg-success" },
};

function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto == null ? "" : String(texto);
  return div.innerHTML;
}

function filtroAtual() {
  const selecao = document.getElementById("filtro-status");
  return selecao ? selecao.value : "";
}

function cardTarefa(tarefa) {
  const info = STATUS_INFO[tarefa.status] || STATUS_INFO["pendente"];
  const titulo = escaparHtml(tarefa.titulo);
  const descricao = escaparHtml(tarefa.descricao || "Sem descrição.");

  const botaoConcluir = tarefa.status !== "concluida"
    ? `<form class="form-concluir" action="/concluir/${tarefa.id}" method="post" data-id="${tarefa.id}">
         <button type="submit" class="btn btn-sm btn-outline-success" title="Concluir">
           <i class="bi bi-check-lg"></i>
         </button>
       </form>`
    : "";

  return `
    <div class="col-md-6 col-xl-4">
      <div class="card tarefa-card h-100 ${info.classe}">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h2 class="h6 card-title mb-0 text-truncate" title="${titulo}">${titulo}</h2>
          <span class="badge ${info.badge}">${info.rotulo}</span>
        </div>
        <div class="card-body">
          <p class="card-text">${descricao}</p>
        </div>
        <div class="card-footer bg-transparent d-flex justify-content-end gap-2">
          ${botaoConcluir}
          <a href="/editar/${tarefa.id}" class="btn btn-sm btn-outline-primary" title="Editar">
            <i class="bi bi-pencil"></i>
          </a>
          <form class="form-excluir" action="/excluir/${tarefa.id}" method="post" data-id="${tarefa.id}">
            <button type="submit" class="btn btn-sm btn-outline-danger" title="Excluir">
              <i class="bi bi-trash"></i>
            </button>
          </form>
        </div>
      </div>
    </div>`;
}

function cardVazio() {
  return `
    <div class="col-12">
      <div class="alert alert-secondary text-center mb-0">
        <i class="bi bi-emoji-smile"></i>
        Nenhuma tarefa por aqui. Clique em "Nova Tarefa" para começar!
      </div>
    </div>`;
}

async function carregarTarefas(status) {
  const url = status
    ? `/api/tarefas?status=${encodeURIComponent(status)}`
    : "/api/tarefas";
  try {
    const resposta = await fetch(url);
    if (!resposta.ok) throw new Error(resposta.statusText);
    const tarefas = await resposta.json();
    const lista = document.getElementById("lista-tarefas");
    if (!lista) return;
    lista.innerHTML = tarefas.length
      ? tarefas.map(cardTarefa).join("")
      : cardVazio();
    document.dispatchEvent(new CustomEvent("tarefas-atualizadas"));
  } catch (erro) {
    console.error("Erro ao carregar tarefas:", erro);
  }
}

async function acaoTarefa(url, metodo, corpo) {
  const opcoes = { method: metodo };
  if (corpo) {
    opcoes.headers = { "Content-Type": "application/json" };
    opcoes.body = JSON.stringify(corpo);
  }
  try {
    const resposta = await fetch(url, opcoes);
    if (!resposta.ok) throw new Error(resposta.statusText);
    await carregarTarefas(filtroAtual());
  } catch (erro) {
    console.error("Falha na operação:", erro);
    alert("Não foi possível concluir a operação.");
  }
}

function atualizarIconeTema(tema) {
  const botao = document.getElementById("botao-tema");
  if (!botao) return;
  botao.innerHTML = tema === "dark"
    ? '<i class="bi bi-sun"></i>'
    : '<i class="bi bi-moon-stars"></i>';
}

document.addEventListener("DOMContentLoaded", function () {
  atualizarIconeTema(document.documentElement.getAttribute("data-bs-theme"));

  document.getElementById("botao-tema").addEventListener("click", function () {
    const atual = document.documentElement.getAttribute("data-bs-theme") === "dark"
      ? "light"
      : "dark";
    document.documentElement.setAttribute("data-bs-theme", atual);
    localStorage.setItem("tema", atual);
    atualizarIconeTema(atual);
  });

  const filtro = document.getElementById("filtro-status");
  if (filtro) {
    filtro.addEventListener("change", function () {
      carregarTarefas(filtro.value);
    });
  }

  document.addEventListener("submit", async function (evento) {
    const formulario = evento.target;

    if (formulario.classList.contains("form-excluir")) {
      evento.preventDefault();
      if (!confirm("Excluir esta tarefa?")) return;
      await acaoTarefa(`/api/tarefas/${formulario.dataset.id}`, "DELETE");
    }

    if (formulario.classList.contains("form-concluir")) {
      evento.preventDefault();
      await acaoTarefa(`/api/tarefas/${formulario.dataset.id}`, "PUT", { status: "concluida" });
    }
  });
});