# Mega Tic - Tac - Toe

This repository contains the code for designing and developing a machine learning model for the Mega Tic-Tac-Toe game.

## Introduction

Have you ever played Tic Tac Toe to settle a debate, only to find yourself engrossed in playing for hours on end because it was just too easy? Then, Mega Tic Tac Toe is for you. While the classic game of Xs and Os is a beloved pastime, its simplicity often leads to draws, leaving no definitive winner. This is where Mega Tic Tac Toe steps in – an amplified version of the classic, designed to challenge players in new and exciting ways. Amidst the sea of machine learning and artificial intelligence projects focusing on conventional Tic Tac Toe, there has yet to be a dedicated pipeline for Mega Tic Tac Toe. Until now.

We're embarking on a pioneering journey to develop the first-ever machine learning pipeline tailored specifically for Mega Tic Tac Toe. This initiative isn't just about creating another game; it's about revolutionizing how we engage with this classic, infusing it with the complexities and challenges that today's AI technologies can offer. Our goal is to build a system that not only understands the intricacies of Mega Tic Tac Toe but also learns and adapts, offering an ever-evolving challenge to human players.

This project is a call to arms for enthusiasts, developers, and thinkers. Together, we will navigate through the nuances of machine learning, deep learning, and artificial intelligence to bring Mega Tic Tac Toe into the realm of advanced computational play. From the initial data collection to the final stages of model training and implementation, this README serves as your comprehensive guide to our development process, our challenges, and our achievements.

Join us on this exciting journey as we pave the way for the future of Mega Tic Tac Toe. Let's transform a simple game of grids into a battleground of wits, strategy, and machine learning brilliance. Welcome to the Mega Tic Tac Toe Machine Learning Pipeline project.

## Rules

### How to Play Mega Tic Tac Toe

Welcome to the comprehensive guide on how to play Mega Tic Tac Toe, an enhanced and more strategic variant of the classic Tic Tac Toe game. Unlike its predecessor, Mega Tic Tac Toe introduces a multi-layered board and strategic play that elevates the game to new heights of complexity and enjoyment. Below are the rules to get you started on this exciting journey.

#### The Board:
Imagine a standard Tic Tac Toe grid. Now, within each of those nine squares, insert another Tic Tac Toe grid. You now have a Mega Tic Tac Toe board, consisting of 9 mini-boards, each with 9 squares.

#### Objective:
The goal is to win three mini-boards in a row, just as you would in the classic game. However, winning a mini-board involves a deeper layer of strategy.

#### Gameplay Rules:

1. **First Move**: Begin by marking one of the small squares in any mini-board. This choice is entirely up to the first player.

2. **Dictated Moves**: Here’s where it gets interesting. The square you choose within a mini-board dictates which mini-board your opponent must play in on their next move. For instance, if you mark the top right square in any mini-board, your opponent must then play in the top right mini-board on their subsequent turn.

3. **Winning a Mini-Board**: To claim a mini-board, you need to align three of your marks (X or O) in a row, whether horizontally, vertically, or diagonally, within that mini-board.

4. **Strategic Depth**: Players must strategize not just where to make a winning move in a mini-board, but also consider how their move will affect the opponent’s position in the overall game, potentially setting them up for a favorable or unfavorable position in the next move.

#### Additional Rules:

- **Claiming a Mini-Board**: If your opponent directs you to a mini-board that has already been won, you are free to choose any other mini-board for your next move. This rule adds a layer of strategy, as sending your opponent to an already won mini-board could be advantageous or disadvantageous depending on the situation.

- **Tied Mini-Boards**: If a mini-board results in a tie (neither player wins it), it's recommended that the mini-board counts for neither player. Alternatively, players can decide before the game starts if a tied mini-board should count for both X and O for a more unconventional gameplay experience.

Mega Tic Tac Toe is more than just a game; it’s a mental exercise in strategic planning, deductive reasoning, and conditional thinking. It transforms the simple act of playing Tic Tac Toe into a complex, engaging, and intellectually stimulating experience. So, next time you find the original game lacking in challenge, turn to Mega Tic Tac Toe for an enriching twist on a familiar pastime.

Enjoy the game, and may the best strategist win!

## Installation

To run the machine learning code, follow these steps:

1. Clone the repository:

    ```shell
    git clone https://github.com/your-username/mega-tic-tac-toe.git
    ```

2. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

3. Run the code:

    ```shell
    python main.py
    ```

## Usage

The machine learning code in this repository provides functionality for training and evaluating models for the Mega Tic-Tac-Toe game. You can use the provided functions and classes to:

- Generate training data by playing against different AI agents or human players.
- Train machine learning models using various algorithms and techniques.
- Evaluate the performance of trained models against different opponents.

## Documentation

For detailed documentation on how to use the machine learning code, refer to the [documentation.md](./documentation.md) file.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](./LICENSE).

## Acknowledgements

We would like to thank the contributors and open-source community for their valuable contributions to this project.

<a href="https://github.com/caterer-z-t/mega-tic-tac-toe/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=caterer-z-t/mega-tic-tac-toe" />
</a>

