# Evolution of the Music Industry

## Abstract

Music has thoroughly evolved in the past decades and so did its industry. Genres appeared as well as new numerous labels that changed the music landscape. New technologies also changed the way music is consumed, both in the music support (numeric, MP3 …) and in the way it can be shared and discovered. To this extent, Discogs is a way for music lovers to keep track of their collection, discover releases but also to buy and sell items on its marketplace. Thus, its database is a great representation of the current music industry and current trends. One interesting particularity is the fact that it focuses more on the “market” dimension than on intrinsic musical characteristics of songs. As music lovers and Discogs users ourselves, we are particularly motivated to use each and every bit of this database !

## Research questions

* How is the disc labels industry distributed (e.g. international record company compared with independant labels) and how did it evolve through the years?
* Does the success of a particular musical genre reflect the rentability/success of its main disc label?
* How do labels follow the general trends of the music industry ?
* What is the evolution of genre popularity based on different measures/metrics?
* From vinyls to *.mp3* files, how did the popularity and profitability of music supports change with new technologies and discoveries?
* How does the popularity of records influence their price overtime ?
* Is it possible to group some Discogs users based on similar genre or releases in their personal collection? Could it reveal some “hidden” relationships between people?

## Dataset
We chose to use Discogs as our Dataset for the project.
Discogs.com is an online records marketplace. It acts as a place for music collectors to buy/sell records, as well as track the evolution of the prices of releases they consider acquiring. Discogs is a social network as well, and users can connect to each other and share the list of their favorite records.
A useful feature of Discogs is its API along with a Python plugin that allows to easily browse and gather information about records, artists and labels from the database. Our aim is to download the latest data files (*XML* format) to create the skeleton of our dataset and then enrich it using the API or web-scraping to gather more relevant informations.


## A list of internal milestones up until project milestone 2

### Collect, clean and understand the data (Nov. 8th)
1. Download the latest update of Discogs files (Records, Masters, Artists and Labels).
2. Gather additional information using the API. If needed, complete the dataset with data scraped from the Discogs website.
3. Filter the entries to keep only relevant records/masters by keeping only vote counts higher than a certain value.
4. Look for inconsistencies or missing values in the dataset. Then, correct or fill them in with web-scraping and remove the remaining incomplete entries.
5. Have a good overview of the data structure, features or possibilities and validate the “Data Gathering” notebook.

### Data analysis (Nov. 15th)
1. Find methods to answer labels and genres oriented research questions and “document” the potential results with relevant plots.
2. Understand the temporal dimension of our data and how it can be exploited.
3. Define structure of “Data Analysis” notebook

### Milestone 2 (Nov. 25th)
1. Clean the code and standardize both plots and results.
2. Discuss data story main orientation and poster possibilities.
3. Start experimenting with clustering methods such as K-Means to identify groups of Discogs users for final milestone.

## Milestone 2
The Jupiter notebook for the ADA Milestone 2 is named "Discogs_Masters".