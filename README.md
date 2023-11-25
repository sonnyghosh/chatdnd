# chatDND - Text-Based Adventure Game

## Introduction

Welcome to chatDND, a text-based adventure game where you embark on an epic journey in a Dungeons & Dragons-style world. In this game, you will navigate through a rich narrative crafted by ChatGPT, your virtual Dungeon Master.

## Getting Started

### Prerequisites

- install requirements.txt

    ```pip install -r requirements.txt```

Make sure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

### Installation

1. Clone this repository:

   ```bash git clone https://github.com/your-username/chatDND.git```


## Testing/Development
- To easily test the website, run the following:
    ```sudo docker-compose up```
- To quit:
    ```sudo docker-compose down```
- Before running ```docker-compose up``` build the api and client images:
  
    ```sudo docker build -f Dockerfile.client -t dnd-client .```
  
    ```sudo docker build -f Dockerfile.api -t dnd-api .```
- To view logs:

    ```sudo docker-compose logs```

- To run API:

    ```sudo docker run -d -p 5000:5000 dnd-api```
    or
    ```sudo docker run -p 5000:5000 dnd-api``` (console output)

- Stop API:

    ```docker ps```
    then
    ```docker stop [CONTAINER ID]```

If you have problems or suggestions please direct them to the cretive director
- stefGPT
