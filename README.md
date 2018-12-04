# flask-movietweetings
Recommender platform for research


A recommender systems platform for running online user experiments. Key features and integrations are as follows:
# Features
- Users can go on the website, rate products and get recommendations
- The base platform is based in Flask-Python. MYSQL integrations are handled through SQLAlchemy.
- The algorithms are pre-built or sourced from the surprise library. Metrics available in MYSQL database.
- Bootstrap template is used for rendering html pages. The frontend is based in HTML, CSS, Javascript.
- Algorithm runs are randomized for each instance(). Metrics available in MYSQL database.
- Advanced Tracking metrics eg user clicks, time on webpages also integrated and available in MYSQL database
- Currently the movietweetings dataset is being used (with metadata scraped from TMDB, but any ratings dataset can be easily incorporated
- The platform has been created specifically to be easy to understand, modify and deploy for research purposes. I've deployed it on AWS Elastic Beanstalk for my research

# To install and run a test server:
Create a virtual environment in python install packages in requirements.txt create database model - python model.py add data - python seed.py (based on your data) run app - python application.py

# Citations necessary for any usage of this platform.


# Citations

- NicolasHug. “NicolasHug/Surprise.” GitHub, 26 Oct. 2018, github.com/NicolasHug/Surprise.
- Sidooms. “Sidooms/MovieTweetings.” GitHub, 4 Dec. 2018, github.com/sidooms/MovieTweetings.
