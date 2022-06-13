FROM node:16
RUN mkdir /app
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone https://github.com/elena-shamshurina/automatisation-frontend
WORKDIR automatisation-frontend
RUN npm install
RUN npm run build
RUN cp -r dist/ ../app/