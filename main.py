from flask import Flask, request, render_template
import pandas as pd
import datetime as dt
from py_tour import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def entry_page():
    return render_template('index.html')


@app.route('/get_dates/', methods=['GET', 'POST'])
def render_message():
    user_city = request.form['user_city']
    user_genre = request.form['user_genre']
    print(user_city)
    print(user_genre)
    df = pd.read_csv(
        "/Users/jakebartolone/ds/metis/make_it_doom/merged_data.csv")
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df.drop(['BIT_artist_id', 'BIT_event_id', 'BIT_venue_city',
            'BIT_venue_country', 'BIT_venue_state', 'sg_venue_id'],
            axis=1, inplace=True)
    df['BIT_event_date'] = \
        df['BIT_event_date'].apply(lambda x: pd.to_datetime(x))
    df['BIT_event_date'] = df['BIT_event_date'].dt.date
    predictions = city_genre_model(df, user_city, user_genre)
    week_recommendations = get_weekly_seasonality(predictions)
    date_recommendations = get_best_dates(predictions)
    return render_template('index.html', weekrec=week_recommendations,
                           daterec=date_recommendations)


if __name__ == '__main__':
    app.run(debug=True)
