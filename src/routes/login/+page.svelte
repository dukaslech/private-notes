<script>
    import { json } from "@sveltejs/kit";
  import "./style.css";

  let usernick = ""
  let userpassword = ""
  let msg = "Login"

  const token = localStorage.getItem("token");
  if(token != "null"){
    window.location.href = "/painel";
  }

  async function logar(){
    const r = await fetch("/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({action:"login", nick: usernick, password: userpassword})
    })

    let j = await r.json()
    console.log(j)
    msg = j.message
    if (j.ok == true){
      localStorage.setItem('token', j.token)
      window.location.href = "/painel";
    }
  }

</script>

<div class="form-login">
  <h1 class="title">{msg}</h1>

  <label class="field">
    <span>Nick</span>
    <input class="input" id="nick" placeholder="seu nick"   bind:value={usernick} />
  </label>

  <label class="field">
    <span>Senha</span>
    <input class="input" id="senha" type="password" placeholder="sua senha" bind:value={userpassword}/>
  </label>

  <button class="btn" on:click={logar()}>Logar</button>
</div>