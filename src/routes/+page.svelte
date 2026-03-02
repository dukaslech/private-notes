<script>
import { onMount } from "svelte";

  let eae = ""
  let user = "";
  let token = "";

  onMount(async () => {
    token = localStorage.getItem("token");

    // 1. Verificação de segurança
    if (!token || token === "semtoken") {
      window.location.href = "/login";
      return; // Interrompe a execução aqui
    }else{
      window.location.href = "/painel";
      return;
    }
  });
</script>
