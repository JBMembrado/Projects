# Evolution of the Music Industry

## [Data Story](https://jbmembrado.github.io/discogs-data/)
All results and plots in the data story come from the Jupyter notebook *Milestone_3.ipynb*. To ensure compatibilty of figures and plots, please make sure you look at the *html* exported version of the notebook: *Milestone_3.html*.

## Abstract

Music has thoroughly evolved in the past decades and so did its industry. Genres appeared as well as new numerous labels that changed the music landscape. New technologies also changed the way music is consumed, both in the music support (numeric, MP3 …) and in the way it can be shared and discovered. To this extent, Discogs is a way for music lovers to keep track of their collection, discover releases but also to buy and sell items on its marketplace. Thus, its database is a great representation of the current music industry and current trends. One interesting particularity is the fact that it focuses more on the “market” dimension than on intrinsic musical characteristics of songs. As music lovers and Discogs users ourselves, we are particularly motivated to use each and every bit of this database !

## Research questions

* How is the disc labels industry distributed (e.g. international record company compared with independant labels) and how did it evolve through the years?
* What are the different representations of a particular genre and how did it change with time?
* How do labels follow the general trends of the music industry?
* What is the evolution of genre distribution based on number of releases?
* From vinyls to *.mp3* files, how did the number and diversity of music supports change with new technologies and discoveries?

## Dataset
We chose to use Discogs as our Dataset for the project.
Discogs.com is an online records marketplace. It acts as a place for music collectors to buy/sell records, as well as track the evolution of the prices of releases they consider acquiring. Discogs is a social network as well, and users can connect to each other and share the list of their favorite records.
A useful feature of Discogs is its API along with a Python plugin that allows to easily browse and gather information about records, artists and labels from the database. Our aim is to download the latest data files (*XML* format) to create the skeleton of our dataset and then enrich it using the API or web-scraping to gather more relevant informations.


## A list of individual contributions to the overall project

This project involved many aspect from data cleaning and filtering to the writting of the data story or the analysis of plots. Here is a little overview of the individual contributions to the project:

- **Jean-Baptiste:** Implementing the API usage of the discogs dataset. Writing the analysis of plots and coding the data story. Presenting the poster.

- **Thomas:** Multiple analysis on the ADA Cluster, web-scrapping on Discogs' website.

- **Jan:** Implementing the plots on the data story. Writing the analysis of plots and coding the data story. Making first drafts of poster designs and layouts.

- **Alex:** Data analysis of genres, styles, labels and formats with plots. Cleaning and updating of the main notebook from Milestone 2.
