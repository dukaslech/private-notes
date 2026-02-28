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
    const r = await fetch("/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "login",
        nick: usernick,
        password: userpassword,
      }),
    });

    let j = await r.json();
    console.log(j);
    msg = j.message;
    if (j.ok == true) {
      localStorage.setItem("token", j.token);
      window.location.href = "/painel";
    }else if (j.ok == false) {
      classe = classeerror
      if (msg = 'Info não existe!'){
        msg = "Nick ou Senha incorretos"
      }
    }
  }
</script>

<div class="form-login">
  <h1 class="title">Login</h1>

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
        placeholder="Batata123@!"
        bind:value={userpassword}
      />
      <button class="btn" on:click={logar()}>Logar</button>
    </label>
  </div>

  
</div>
