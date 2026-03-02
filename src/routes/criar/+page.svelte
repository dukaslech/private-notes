<script>
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import "./style.css";

    let token = ""
    let title = "";
    let body = "";
    let pass = "";
    let userid = "";
    onMount(async () => {
        token = localStorage.getItem("token");

        if (!token || token === "semtoken") {
            window.location.href = "/login";
            return;
        }
        await fetchInfos();
    });

    async function fetchInfos() {
        try {
            const r = await fetch(`/api/info/${encodeURIComponent(token)}`);
            const j = await r.json();
            eae = j;
            console.log(j);

            if (r.ok) {
                userid = j.user.id;
            } else {
                console.error("Erro na API:", j.message);
            }
        } catch (err) {
            console.error("Erro de conexão:", err);
        }
    }

    async function criar() {
        const ra = await fetch(`/api/info/${encodeURIComponent(token)}`);
        const ja = await ra.json();
        userid = ja.user.id
        const r = await fetch("/api/note", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                action: "create",
                title: title,
                body: body,
                password: pass,
                userid: userid,
            }),
        });

        let j = await r.json();
        console.log(j);
        if(j.ok == true){
            window.location.href = "/painel"
        }else{
            window.location.href = "/criar"
        }
    }
</script>

<div class="card">
    <div class="inputs">
        <input
            bind:value={title}
            class="title"
            placeholder="Como criar uma nota"
        />
        <input
            bind:value={pass}
            class="title"
            placeholder="SenhaMuitoLegal@!"
            type="password"
        />
        <button class="btn-create" on:click={criar}>Criar</button>
    </div>
    <textarea
        bind:value={body}
        class="body"
        placeholder="Bom, pra você criar uma nota é só não ser burro porra, seja inteligente"
    ></textarea>
</div>
