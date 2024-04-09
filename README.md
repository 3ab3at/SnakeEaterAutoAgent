# Snake Eater

## Description

Automatic ML model for playing Snake Eater. 
The game implementation was last modified in January 2024 by José Carlos Pulido for the Machine Learning Classes at the University Carlos III of Madrid.

## Features

- Automatic snake movement based on BFS algorithm.
- Extract Features from the game to train models to play the game using Weka.
- Training of different ML models to play the game `Play.py` (currently j48.model)
- Regression models for predicting snake movements and score `Predict.py`
- Colorful graphical interface.

## Setup

1. Make sure you have Python and PyGame installed.
2. Clone the repository.
3. Run `python Play.py` to start the game with the j48 model playing.
4. Run `Predict.py` to start the regression model for score prediction.
