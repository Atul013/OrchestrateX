FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the built frontend and server
COPY dist/ ./dist/
COPY server.js ./

EXPOSE 8080

CMD ["node", "server.js"]