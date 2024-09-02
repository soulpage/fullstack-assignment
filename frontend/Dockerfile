# Stage 1: Build the app
FROM node:18-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Stage 2: Serve the app with a lightweight web server
FROM node:18-alpine AS runner

# Set the working directory
WORKDIR /app

# Install only production dependencies
COPY --from=builder /app/package*.json ./
RUN npm install --production

# Copy the built Next.js application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Expose the port the app runs on
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]
