# online-chess-game

A functional online chess game that allows players to engage in matches against each other in real-time or challenge a computer opponent. Developed within 12 hours as a challenge, this project showcases real-time capabilities, essential chess game logic, and an intuitive frontend js and chess.js library , paired with a Django backend for server-side logic using Stockfish engine .

## Features

### Core Features

- #### Player vs. Player Mode (Real-Time):

  - Players can start a chess game against each other.
  - Real-time updates for moves using WebSockets technology.
  - Turn rotation and chessboard display are implemented correctly.

- #### Player vs. AI Mode:

  - Players can challenge one of two computer opponent.
  - in the easy mode the computer makes legal moves based on random or beginner-level logic.
  - in the difficult mode you play against stockfish engine latest level you can't win

- #### Game Logic and Move Validation:
  - Enforces chess rules: legal moves for all pieces, check and checkmate detection, stalemate and draw conditions.
  - Invalid moves are prevented, with visual feedback provided for illegal actions.
- #### Chat Room
  - players can communicate with each other in real-time through an integrated chat room.
- #### Timers:

  - Each player has a countdown timer, switching based on whose turn it is.
  - The game declares the other player as the winner if a timer runs out.

- #### User Interface :
  - visually clear UI displaying the chessboard,move history,chat room, timers, and buttons for starting new games.

## Demo

![Alt Text](https://raw.githubusercontent.com/mena18/online-chess-game/refs/heads/main/demo/demo.gif)

## How can you use it

### Install Redis or use Docker

```console
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

### clone the project

```console
git clone https://github.com/mena18/online-chess-game.git
cd online-chess-game/backend
```

### download stockfish engine

install stockfish engine on your operating system then create `.env` file and add your stockfish engine path to it
`STOCKFISH_PATH=YOUR_PATH`

### install requirements

```console
pip install -r requirements.txt
```

### Run Server

```console
python manage.py runserver
```

## Future Improvements

Here are several enhancements planned for the future to improve the project:

- **User Authentication**: Implement user registration and login functionalities to save game results and player profiles.
- **Database** : use sqlite to store all the games and moves for future reference so player can look for the game later on
- **Game Reconnection**: Allow players to reconnect to ongoing games if they disconnect accidentally.
- **multiple AI Levels**: use multiple levels for the Ai instead of having very easy level (random) and the most difficult level on the other hand
- **Game Analysis Tools**: Integrate tools that analyze players' games post-match to provide insights and improvement suggestions.
- **Customizable Chessboards**: Enable players to choose different themes or styles for the chessboard and pieces.
- **Mobile Responsiveness**: Enhance the UI for better performance and usability on mobile devices.
- **Game Replay Feature**: Implement functionality to replay completed games for review and learning purposes.

## Acknowledgments

Special thanks to the libraries and resources used to facilitate the development of this chess game, including

- Django & Django channels
- Stockfish
- Chess.js
- Chessboard.js
