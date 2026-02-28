<script>
import { onMount } from "svelte";
  import "./style.css";

  let eae = ""
  let user = "";
  let token = "";

  onMount(async () => {
    token = localStorage.getItem("token");

    // 1. Verificação de segurança
    if (!token || token === "semtoken") {
      window.location.href = "/login";
      return; // Interrompe a execução aqui
    }

    // 2. Só busca as infos se passar pelo check acima
    await fetchInfos();
  });

  async function fetchInfos() {
    try {
      const r = await fetch(`/api/info/${encodeURIComponent(token)}`);
      const j = await r.json();
      eae = j
      console.log(j)
      
      if (r.ok) {
        user = j.user.nick;
      } else {
        console.error("Erro na API:", j.message);
      }
    } catch (err) {
      console.error("Erro de conexão:", err);
    }
  }
</script>

<div class="wrap">
  <header class="topbar">
    <h1 class="title">BEM VINDO <span class="user">{user}</span></h1>
    <button class="btn">CRIAR</button>
  </header>

  <main class="grid">
    {#each eae.notes as note}
    <a href='/nota/?id=${note.id}'>
      <article class="card" aria-label={note.id}>
        <h3 class="card-title">{note.title}</h3>
      </article>
    </a>
    {/each}
  </main>
</div>