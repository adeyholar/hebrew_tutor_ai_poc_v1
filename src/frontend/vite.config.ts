// vite.config.ts - Vite configuration for HebRabbAI frontend
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';  // Node path for Windows-safe resolution (TS types handled in tsconfig)

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Modular alias for data\text - scalable, no hardcoding; resolves nested path
      '@data': resolve(__dirname, '../../data/text'),
      // Stub for audio (future TTS WAVs in data\audio)
      '@audio': resolve(__dirname, '../../data/audio'),
    },
  },
  server: {
    host: true,  // Network binding (Phase 1)
    port: 5173,
  },
  css: {
    postcss: './postcss.config.js',  // Tailwind from Phase 1
  },
  build: {
    outDir: 'dist',  // Scalable output
    sourcemap: true,  // Debugging
  },
  // PWA stub (enable vite-plugin-pwa for offline in Phase 3)
});