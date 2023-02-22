FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache
EXPOSE ${PORT}
CMD ["npm", "start"]