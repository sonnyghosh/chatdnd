FROM python:3.9
WORKDIR /app

COPY /api/requirements.txt api/api.py api/.flaskenv ./
RUN pip install -r ./requirements.txt
EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]


# FROM node as build-setup
# WORKDIR /app
# ENV PATH /app/node_modules/.bin:$PATH
# COPY package.json yarn.lock ./
# COPY ./src ./src
# COPY ./public ./public
# RUN yarn install
# RUN yarn build

# FROM nginx
# COPY --from=build-setup /app/build /usr/share/nginx/html
# COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf
