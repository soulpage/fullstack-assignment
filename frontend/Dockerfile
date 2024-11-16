FROM node:18.20.4-slim AS base
LABEL stage="install"
WORKDIR /install
COPY package.json .
RUN npm install -g npm@10.9.0
RUN npm install


FROM  node:18.20.4-slim AS build
LABEL stage="build"
WORKDIR /build
COPY --from=base /install/node_modules ./node_modules
COPY . .
RUN npm install -g npm@10.9.0
RUN npm run build

FROM node:18.20-alpine
LABEL stage="deploy"
MAINTAINER ujwal.pachghare
WORKDIR /usr/bin/app
ENV NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000" 
COPY --from=build /build/node_modules ./node_modules
COPY --from=build /build/.next ./.next
COPY . .
EXPOSE 3000
CMD ["npm","start"]
