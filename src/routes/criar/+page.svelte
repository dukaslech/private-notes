<script>
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import "./style.css";

    let title = "";
    let body = ""
    let pass = "";
    onMount(async () => {
        token = localStorage.getItem("token");
        
        if (!token || token === "semtoken") {
            window.location.href = "/login";
            return;
        }
    });
</script>

<div class="card">
    <div class="inputs">
        <input class="title" placeholder="Como criar uma nota" />
        <input class="Senha" placeholder="SenhaMuitoLegal@!" />
        <button class="btn-create">Criar</button>
    </div>
    <textarea
        class="body"
        placeholder="Bom, pra você criar uma nota é só não ser burro porra, seja inteligente"
    ></textarea>
</div>
