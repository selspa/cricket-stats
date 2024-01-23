FROM node:alpine
ENV NODE_OPTIONS=--openssl-legacy-provider
WORKDIR /app
COPY . /app
EXPOSE 3000
CMD ["npm", "start"]
