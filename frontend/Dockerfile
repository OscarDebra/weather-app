FROM node:20 AS builder

WORKDIR /app

# 1. Copy dependency files first
COPY package.json package-lock.json ./

# 2. Install dependencies
RUN npm install

# 3. Copy source code
COPY . .

# 4. Build
RUN npm run build

# 5. Serve with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html