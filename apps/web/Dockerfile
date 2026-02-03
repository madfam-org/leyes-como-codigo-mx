# apps/web/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY apps/web/package.json apps/web/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY apps/web .

# Build the app
RUN npm run build

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
