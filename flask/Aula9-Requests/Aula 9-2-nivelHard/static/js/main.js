/**
 * Fluxo 2 — validação de senha via fetch (Request HTTP + resposta JSON)
 */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-senha-fluxo2");
    if (!form) return;

    const msgErro = document.getElementById("msg-erro");
    const btn = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const senha = document.getElementById("senha").value.trim();
        if (!senha) return;

        if (btn) {
            btn.disabled = true;
            btn.textContent = "Verificando...";
        }
        if (msgErro) msgErro.classList.add("hidden");

        try {
            const resposta = await fetch("/api/validar-senha", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ fluxo: "fluxo2", senha: senha }),
            });

            const dados = await resposta.json();

            // redirect vindo do JSON: Flask montou a URL com url_for; o JS só navega até ela
            if (dados.ok) {
                window.location.href = dados.redirect;
                return;
            }

            if (msgErro) {
                msgErro.textContent = dados.mensagem || "Senha incorreta.";
                msgErro.classList.remove("hidden");
            }
        } catch (erro) {
            if (msgErro) {
                msgErro.textContent = "Erro na requisição. Servidor ativo?";
                msgErro.classList.remove("hidden");
            }
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.textContent = "Entrar";
            }
        }
    });
});
