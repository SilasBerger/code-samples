# Sample Code of Relevant Projects
## General
The code of the past projects (bernmobil-open-data, visually-exploring-scientific-communities) hasn't been maintained after the end of the respective projects. It is therefore not guaranteed to be runnable out-of-the-box.

## Projects
## twitter-localization
_Master's thesis at the HumanTech Institute at HEIA-FR, September 2018 - now_

This project aims to explore techniques for determining the location of origin of Twitter users and tweets where this information is not given through GPS data or specified in the user’s profile. As a first step, we want to determine whether or not a given user or tweet is Swiss.

For our initial model, we use a list of Twitter users that we refer to as "Swiss influencers". These are well-known personalities, brands, etc. which we suspect to be mostly followed by Swiss users. For instance, Roger Federer likely has Twitter followers from around the world, which makes him unsuitable as an influencer, even though he is Swiss. On the other hand, entities such as domestic newspapers, Swiss politicians, or lesser-known Swiss athletes are less likely to be followed by Twitter users outside of Switzerland, which makes them more suitable for the purpose.

The core technologies include Python, MongoDB, Neo4j and Flask for the backend, as well as Node.js and Vue.js for the frontend.

## visually-exploring-scientific-communities
_Bachelor's thesis at the Software Composition Group at UniBE, September 2016 - August 2017_

Since Pharo doesn't work well with Git, the project folder can be found [here](https://1drv.ms/f/s!AnAsJI7izZ1QhIpXNJTIZ7TfvPehBw). The code is also available as a _Monticello_ repository (Pharo-specific version control system) on [SmalltalkHub](http://smalltalkhub.com/#!/~SilasBerger/ExtendedEggShell/).

Implemented a Pharo program called _ExtendedEggShell_, which aimed to generate graph representations of scientific communities. The goal was to visually answer queries about these communities, their core research areas, and their underlying collaboration networks. As a basis upon which to model scientific communities, we used tools to extract metadata from PDF files of papers published within these communities.

More information on the motivation behind ExtendedEggShell, its implementation, examples, challenges, and results can be found in my bachelor's thesis, which is included in the project folder (Berg17a.pdf).

The project was implemented in Pharo Smalltalk, using the Moose toolset. The visualizations were created with Roassal, which is part of Moose.

### bernmobil-open-data
_Course project for the "Open Data" course at UniBE, February 2016 - June 2016_<br>
This project was developed in collaboration with Bernmobil and aimed to provide visualizations of their open data. The main focus was on generating different views of Bernmobil’s historic data on delays and cancellations across their various courses. We decided to use a map view, where we marked all of Bernmobil's courses and styled each marking according the number of cancellations or delays that occurred during the time covered by the available dataset.

Users also had the option to filter the data (and consequently, the resulting visualization) for specific months, or for specific types causes for cancellations and delays, such as technical malfunction, traffic jam, weather conditions, or road blocks due to events or protests. This allowed users to gain a visual impression of which courses are mostly affected by which types of disturbances, with respect to specific months or seasons.

The project folder contains an image called `preview.png`, which a screenshot of the map view that was taken during development.

The core technologies were HTML, CSS, JavaScript and D3.js for the visualization.
