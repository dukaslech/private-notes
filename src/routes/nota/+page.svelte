<script>
  import { onMount } from "svelte";
  import "./style.css";

  onMount(async () => {

  })

  function autoResize(e) {
    const el = e.currentTarget;
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  }

</script>

<div class="page">
  <div class="card">
    <input
      class="title"
      type="text"
      placeholder="TÍTULO"
      //bind:value={'eae'}
    />

    <textarea
      class="body"
      placeholder="BODY"
      //bind:value={'eae'}
      rows="6"
      on:input={autoResize}
    ></textarea>
  </div>
</div>