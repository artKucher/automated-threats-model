FROM node:16
RUN mkdir /app
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone https://github.com/elena-shamshurina/automatisation-frontend
WORKDIR automatisation-frontend
RUN cp ../app/.environment src/environments/environment.prod.ts
RUN npm install
RUN npm run build
RUN rm -rf ../app/dist
RUN cp -r dist/ ../app/