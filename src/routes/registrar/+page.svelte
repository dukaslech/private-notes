<script>
  import { json } from "@sveltejs/kit";
  import "./style.css";

  let usernick = "";
  let userpassword = "";
  let msg = "Login";
  let passform = "";
  let classenormal = "disable"
  let classeerror = "error"
  let classe = classenormal

  const token = localStorage.getItem("token");
  if (token && token !== "semtoken") {
    window.location.href = "/painel";
  }
  async function logar() {
    const r = await fetch("https://private-notes-chi.vercel.app/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "register",
        nick: usernick,
        password: userpassword,
      }),
    });

    let j = await r.json();
    console.log(j);
    msg = j.message;
    if (j.ok == true) {
      window.location.href = "/login";
    }else if (j.ok == false) {
      classe = classeerror
      if (msg = 'Info não existe!'){
        msg = "Nick ou Senha incorretos"
      }else {
        msg = "Error no servidor, contate o suporte do site"
      }
    }
  }
</script>

<div class="form-login">
  <h1 class="title">Registrar</h1>

  <div class={classe}>
    <h1 class="error-title">&#9888; Erro!</h1>
    <p>{msg}</p>
  </div>
  <div class="div-input">
    <label class="field">
      <span>Nick</span>
      <input
        class="input"
        id="nick"
        placeholder="Duka"
        bind:value={usernick}
      />
    </label>

    <label class="field">
      <span>Senha</span>
      <input
        class="input"
        id="senha"
        type="password"
        placeholder="Abacate123@!"
        bind:value={userpassword}
      />
      <button class="btn" on:click={logar()}>Registrar</button>
    </label>
    <a href="/login" data-sveltekit-reload data-sveltekit-preload-data="off">Logar</a>
  </div>

  
</div>
