<script>
    import { page } from '$app/stores';
    import { onMount } from "svelte";
    import "./style.css";

    let title = "TÍTULO";
    let body = `BODY
    Linha 2
    Linha 3`;
    // estado da UI
    let pass = "";
    let unlocked = false;
    let msg = "";   
    let id_nota = ""

    onMount(async () => {
        id_nota = $page.url.searchParams.get('id')
        console.log(id_nota)
    });

    async function noteview(id, password) {
        let r = await fetch("https://private-notes-chi.vercel.app/api/note",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    action: "view",
                    noteid: id,
                    password: password,
                }),
            })
        let j = await r.json()
        console.log(j)
        if(j.message == 'Info não existe!'){
            msg = "Nota ou senha invalida!"
        }else if(j.message == 'Campos incompletos'){
            msg = "Digite uma senha"
        }else if(j.ok == true){
            title = j.title
            body = j.body
            unlocked = true
        }
    }

    function autoResize(e) {
        const el = e.currentTarget;
        el.style.height = "auto";
        el.style.height = el.scrollHeight + "px";
    }

</script>

<div class="page">
    <!-- janela de senha -->
    <div class="passform" class:disable-passform={unlocked}>
        <div class="passform-inner">
            <h2 class="pass-title">Senha da nota</h2>

            <input
                class="pass-input"
                type="password"
                placeholder="Digite a senha"
                bind:value={pass}
            />

            <button class="pass-btn" on:click={() => noteview(id_nota, pass)}>OK</button>

            {#if msg}
                <p class="pass-msg">{msg}</p>
            {/if}
        </div>
    </div>

    <!-- conteúdo da nota -->
    <div class="card">
        <h1 class="title">{title}</h1>
        <div class="body">{body}</div>
    </div>
</div>
