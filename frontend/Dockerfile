FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Build application
RUN npm run build

EXPOSE 3000

# Run the application
CMD ["npm","run", "start"]
