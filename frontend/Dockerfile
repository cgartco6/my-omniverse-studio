FROM node:18-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --prefer-offline --no-audit

COPY . .

EXPOSE 3000

ENV REACT_APP_API_URL=http://localhost:8000

CMD ["npm", "start"]
