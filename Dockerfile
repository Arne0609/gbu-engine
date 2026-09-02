# GBU 4.0 Bewertungsengine – REST-API (Node 22, TypeScript ohne Build-Schritt)
FROM node:22-slim

WORKDIR /app

# Nur Manifeste zuerst (bessere Layer-Caches)
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev || npm install --omit=dev

# Quellen (flutter_ui, dart_engine, Tests etc. sind via .dockerignore ausgeschlossen)
COPY . .

ENV NODE_ENV=production
# Railway setzt PORT selbst; lokal Fallback 8787.
EXPOSE 8787

# node führt die .ts-Dateien direkt aus (Type Stripping, kein Transpile).
CMD ["node", "--experimental-strip-types", "server.ts"]
