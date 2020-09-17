FROM node:lts-alpine as base
WORKDIR /app

FROM base as dependencies
WORKDIR /app
## Install build toolchain, install node deps and compile native add-ons
RUN apk add --no-cache python make g++
RUN apk add --no-cache git
COPY ./package*.json ./
RUN npm install

FROM dependencies as app-build
WORKDIR /app
COPY ./tsconfig.json ./
COPY ./lib ./lib
## we use Typescript, this runs the transpilation
RUN npm run build 

FROM dependencies as app-backend
WORKDIR /app
COPY --from=app-build /app/node_modules ./node_modules
COPY --from=app-build /app/dist ./dist
COPY --from=app-build /app/package*.json ./
COPY ./views ./views
COPY ./public ./public

EXPOSE 5000

CMD ["npm", "run", "deploy"]