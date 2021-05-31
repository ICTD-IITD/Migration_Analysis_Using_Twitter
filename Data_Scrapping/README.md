 # Scraping the data of Twitter users on the basis of locations

The code in this repository can be used to get the data of tweets and users, based on their geolocations, i.e. their latitude and longitude.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

* This app requires the use of Python 3+
* Use the requirements.txt folder to find the packages required to run this project

    1. Setup MongoDB to run on your local computer.
    2. Make sure that the MongoDB server is up and running.
    3. Run the code in run.py to get tweets.
    4. Enjoy!  

### Prerequisites

* Python 3+
* Virtualenv
* MongoDB
* Homebrew

### Installing

Firstly install Homebrew, the package manager for Macintosh. Paste the below code snippet in the MocOS terminal. Ignore if homebrew is already installed

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Now install to install mongodb

```
brew tap mongodb/brew && brew install mongodb-community 
```
Install Python as well

```
brew install python3
```

We now need to install the packages required. To do so, we would first need to create a virtualenv.

```
cd Desktop && git clone git@github.com:saphal1998/twitter-scraping.git && cd twitter_scraping
virtualenv .
```

Now that the virtualenv is set up, we can install the required packages using, 

```
pip install -r requirements.txt
```

All the packages should now be successfully installed. We are now ready to run the scripts. However, we first need to run our MongoDB server

```
brew services start mongodb-community
```

We can now successfully interact with the MongoDB database

To stop the server

```
brew services stop mongodb-community
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python](https://docs.python.org/3/) - The programming language used
* [Git](https://www.git-scm.com/doc) - Version Control Management
* [MongoDB](https://docs.mongodb.com) - Database used

## Authors

* **Saphal Patro** - *Initial work* - [saphal1998](https://github.com/saphal1998)
* **Siddharth Basu** - *Initial work* - [siddharth-basu98](https://github.com/siddharth-basu98)
