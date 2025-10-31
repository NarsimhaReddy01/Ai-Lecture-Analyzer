# ===============================
# 1️⃣ Build Stage - React (Node)
# ===============================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json* yarn.lock* ./

# Install dependencies using clean cache
RUN npm ci --legacy-peer-deps

# Copy the full app source
COPY . .

# Build the production bundle
RUN npm run build

# ===============================
# 2️⃣ Serve Stage - Nginx
# ===============================
FROM nginx:1.25-alpine

# Copy compiled React build into Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy optional custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the frontend port
EXPOSE 80

# Launch Nginx
CMD ["nginx", "-g", "daemon off;"]
