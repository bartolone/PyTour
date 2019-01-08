# PyTour
PyTour: a Python-powered band tour-planning assistant

PyTour delivers recommendations via a Flask app for when bands should plan to come to a given city on tour, based on that band's genre. Users select a genre and a city, and PyTour lists the best and worst dates for a band of that genre to book a show in that city.

These recommendations are based on a time series model that includes the best gig -- based on the prestige of the venue -- booked by a band of a given genre on a given date in a given city, with data going back several years. The model uses this information to make predictions, incorporating both weekly and yearly seasonality, about which dates bands of a genre can expect to book the best shows in that city.

PyTour uses data from two APIs to construct a file containing approximately one million gigs for around 40,000 artists between 2013 and 2018. SeatGeek, a ticket-reselling site, offers artist and venue prestige scores (based on the desirability of tickets for the artist or venue) and categorizes artists into genres. Bandsintown, a concert aggregator, provides information on past (and future) gigs by artist, including venue. PyTour uses FB Prophet, a Python package for modeling time series data, to model how the quality of gigs booked by artists of a given genre vary over the year and over days of the week and make predictions for good and bad days in the future. Because every city's musical scene differs, PyTour constructs a new model for each combination of genre and city in real time based on user input.
