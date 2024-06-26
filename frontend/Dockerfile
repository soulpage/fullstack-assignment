FROM node:latest

WORKDIR /nextjs-app

COPY package.json ./

COPY package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3002

CMD ["npm", "start"]
