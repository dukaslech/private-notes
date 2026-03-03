import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
    proxy: {
      '/api': 'https://private-notes-chi.vercel.app'
    }
  }
});
