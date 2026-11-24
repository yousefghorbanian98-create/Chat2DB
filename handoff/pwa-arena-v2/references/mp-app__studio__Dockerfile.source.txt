# Muscle Paradise — ایمیج استودیو (nginx + SPA + پراکسی API)
# ساخت از ریشهٔ مخزن: docker build -f mp-app/studio/Dockerfile -t mp-studio .
FROM node:20-alpine AS build
WORKDIR /src
COPY mp-app/studio/ ./
RUN npm ci && npm run build

FROM nginx:1.27-alpine
COPY mp-app/studio/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist /usr/share/nginx/html
EXPOSE 80
