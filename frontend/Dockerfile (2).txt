# Use official Node.js image as the base image
FROM node:latest

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application for production
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Command to run the Next.js application
CMD ["npm", "start"]

