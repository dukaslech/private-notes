<script>
  import { json } from "@sveltejs/kit";
  import "./style.css";

  let user = "Login"

  const token = localStorage.getItem("token");
  if(token == "null"){
    window.location.href = "/login";
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

<div class="wrap">
  <header class="topbar">
    <h1 class="title">BEM VINDO <span class="user">{user}</span></h1>
    <button class="btn">CRIAR</button>
  </header>

  <main class="grid">
      <article class="card" aria-label={"nota " +1}>
        <h3 class="card-title">eae</h3>
      </article>
  </main>
</div>