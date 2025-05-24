# Video Game Database

## Description:

The Video Game database is a web application that allows you to find details about any video game you desire. You can also check out the top and trending games on the website. The project is built mainly using Flask and the IGDB API.

### Features:

- Search for any game by it's name
- Game Details: Name, Cover Art, Summary, Release Dates, Genres, Platforms, and and description of a game can be viewed.
- Top and Trending Games: You can view the top and trending games on the website.

### File Descriptions:

- **app.py**: The main file that runs the Flask application. The python script is used to manage the backend of the website including the routes, the database, and the IGDB API.

- **styles.css**: The CSS file is used to style the entire website which includes all the different pages and components.

- **base.html**: The base template that is used for all the pages which includes the navigation bar.
- **index.html**: Main page of the website which includes a search bar to search for any game by it's name and a navigation bar to navigate to the top and trending games page.
- **search_results.html**: The page that displays the search results for the searched name upto 20 results per page.
- **game_detail.html**: The page that displays the details of the selected game including the name, cover art, a description, release date, genres, and platforms.
- **top_games.html**: The page that displays the top games of all time.
- **trending_games.html**: The page that displays the current trending games.

### Challenges Faced:

- **Efficiently managing the API calls**: Implemented caching mechanisms to reduce redundant requests to the IGDB API. Also, implemented pagination to reduce the number of requests to the API. Other problems like the API returning low quality images and the API returning low quality data for the games were also faced and solved by specifying the quality required in the API request.

- **Designing an intuitive user interface**: The design of the website was a bit challenging as I had to make sure that the website is aesthetically pleasing and also functional with all the API data. I had to make sure that the website is responsive and that the user experience is smooth.

- **Handling Errors and Edge Cases**: The website should handle errors and edge cases gracefully. For example, if the user searches for a game that doesn't exist, the website should display a message to the user.

This project demonstrates the integration of web development, API handling, and user-centered design to create a functional and visually appealing application while showcasing all the skills acquired throughout the CS50 course.
