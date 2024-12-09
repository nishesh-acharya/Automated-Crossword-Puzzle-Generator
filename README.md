# Automated Crossword Puzzle Generator
#### Video Demo:  https://www.youtube.com/watch?v=_HlRideRQCk
#### Description: 
The application includes a sign-in feature and focuses on generating crossword puzzles dynamically. Here's a breakdown of the key features and functionalities I implemented:

#### User Authentication and Sign-Up
For user authentication and sign-up functionality, I utilized Flask's session management and secure user authentication. The following tasks were completed:

- Implemented user registration, login, and logout functionality.
- Created a database using SQLAlchemy to store user information securely, including usernames and hashed passwords.
- Developed Flask routes to handle user registration, login, and logout requests.
- Designed and implemented HTML templates for the registration and login pages, incorporating user input forms.

#### Crossword Puzzle Generation
The core aspect of the project was the automatic generation of crossword puzzles. To achieve this, I developed a backend algorithm that generates puzzles based on words and clues obtained from an API. Here's what I accomplished:

- Implemented a Flask route to handle puzzle generation requests, which accepts a list of words and clues as input.
- Utilized the algorithm to generate crossword puzzles dynamically.
- Returned the generated puzzles in JSON format, ready for rendering and gameplay.

#### Rendering the Crossword Puzzle
To display the generated crossword puzzle, I focused on creating an interactive and visually appealing user interface. Here's an overview of what was done:

- Designed an HTML template for the crossword puzzle page, where the puzzle grid is displayed.
- Dynamically retrieved the generated puzzle data and rendered the crossword grid on the HTML page.
- Displayed clues associated with each word in the grid, enabling users to interact with the puzzle effectively.

#### User Gameplay and Interaction
To enhance user experience and enable gameplay functionality, I implemented JavaScript features. The following functionalities were implemented:

- Developed JavaScript functionality to handle user interaction with the crossword puzzle grid.
- Enabled users to input letters by clicking on grid cells, validating their inputs, and providing immediate feedback.
- Created JavaScript functions to check user-inputted words against the correct solution, highlighting correct/incorrect letters, and handling puzzle completion.
- Developed a scoring system to track and display user scores based on accuracy.

#### Additional Features
To further enhance the overall user experience, I’ve added several additional features to the application:

- Included a leaderboard feature to track and display high scores achieved by users.
- Provided users with the option to customize the puzzle difficulty level based on their preferences.

