# chatDND - Text-Based Adventure Game

## Introduction

Welcome to chatDND, a text-based adventure game where you embark on an epic journey in a Dungeons & Dragons-style world. In this game, you will navigate through a rich narrative crafted by ChatGPT, your virtual Dungeon Master.

## Getting Started

### Prerequisites

- install requirements.txt

    ```pip install -r requirements.txt```

### Installation

1. Clone this repository:

   ```bash git clone https://github.com/your-username/chatDND.git```

## Testing/Development
- To easily test the website, run the following:
    ```docker-compose up```
- To quit:
    ```docker-compose down```
- If you haven't done so, build the api and client images like this:
  
    ```docker build -f Dockerfile.client -t dnd-client .```
  
    ```docker build -f Dockerfile.api -t dnd-api .```
