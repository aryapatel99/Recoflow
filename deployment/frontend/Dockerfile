FROM node:22-alpine

WORKDIR /app

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_TELEMETRY_DISABLED=1

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build
RUN npm prune --omit=dev && rm -rf .next/cache

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs
RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3001
CMD ["npm", "run", "start"]
