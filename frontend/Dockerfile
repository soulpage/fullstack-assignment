FROM node:20.14.0-alpine

# Set the working directory
WORKDIR /fullstack-assignment/frontend

# First copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install
COPY . .
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
