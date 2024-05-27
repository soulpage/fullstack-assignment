
# Use the Alpine version of the Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# First copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source code to the working directory
COPY . .

# Build the application
RUN npm run build

# Next.js listens on port 3000 by default
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
