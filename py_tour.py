import numpy as np
import datetime as dt
from fbprophet import Prophet


def city_genre_model(df, city, genre):
    city_genre_df = df.loc[(df['genre'] == genre) & (df['venue_city'] == city)]
    agg_df = city_genre_df.groupby('BIT_event_date', as_index=False).agg('max')
    prophet_df = agg_df[['BIT_event_date', 'venue_score']].rename(
        columns={'BIT_event_date': 'ds', 'venue_score': 'y'})
    prophet_df = prophet_df[(prophet_df['ds'] < dt.date(2018, 12, 1))]
    prophet_df = prophet_df[(prophet_df['y'] > 0)]
    prophet_df = prophet_df[(prophet_df['y'] < .8)]
    print(prophet_df.shape)
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    return forecast


def convert_week_index_to_text(ind_list, remaining_days, good_or_bad):
    if len(ind_list) == 5:
        day_list = "<b>" + remaining_days[ind_list[0]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[1]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[2]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[3]] \
            + "</b>, and <b>" \
            + remaining_days[ind_list[4]] \
            + "</b> are also " \
            + good_or_bad + " days to play"
    elif len(ind_list) == 4:
        day_list = "<b>" + remaining_days[ind_list[0]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[1]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[2]] \
            + "</b>, and <b>" \
            + remaining_days[ind_list[3]] \
            + "</b> are also " \
            + good_or_bad + " days to play"
    elif len(ind_list) == 3:
        day_list = "<b>" + remaining_days[ind_list[0]] \
            + "</b>, <b>" \
            + remaining_days[ind_list[1]] \
            + "</b>, and <b>" \
            + remaining_days[ind_list[2]] \
            + "</b> are also " \
            + good_or_bad + " days to play"
    elif len(ind_list) == 2:
        day_list = "<b>" + remaining_days[ind_list[0]] \
            + "</b> and <b>" \
            + remaining_days[ind_list[1]] \
            + "</b> are also " \
            + good_or_bad + " days to play"
    else:
        day_list = "<b>" + remaining_days[ind_list[0]] \
            + "</b> is also a " \
            + good_or_bad + " day to play"
    return day_list


def string_weekly_seasonality(max_loc, min_loc, other_good_loc, other_bad_loc):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']
    best_string = "The best day of the week to play is <b>" \
        + days_of_week[max_loc] + "</b>"
    worst_string = "The worst day of the week to play is <b>" \
        + days_of_week[min_loc] + "</b>"
    pop1 = max(max_loc, min_loc)
    pop2 = min(max_loc, min_loc)
    days_of_week.pop(pop1)
    days_of_week.pop(pop2)
    if len(other_good_loc) == 0 & len(other_bad_loc) == 0:
        other_string = "No other day of the week is particularly good or bad"
    elif len(other_good_loc) == 0:
        other_string = \
            convert_week_index_to_text(other_bad_loc, days_of_week, 'bad')
    elif len(other_bad_loc) == 0:
        other_string = \
            convert_week_index_to_text(other_good_loc, days_of_week, 'good')
    else:
        other_string = \
            convert_week_index_to_text(other_good_loc, days_of_week, 'good') \
            + ", but " + \
            convert_week_index_to_text(other_bad_loc, days_of_week, 'bad')
    return best_string, worst_string, other_string


def get_weekly_seasonality(preds_df):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']
    weekly_seasn = \
        [preds_df.loc[(preds_df['ds'] == dt.date(2018, 12, 31))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 1))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 2))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 3))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 4))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 5))]
            .iloc[0]['weekly'],
            preds_df.loc[(preds_df['ds'] == dt.date(2019, 1, 6))]
            .iloc[0]['weekly']
         ]
    max_index = np.argmax(weekly_seasn)
    min_index = np.argmin(weekly_seasn)
    pop1 = max(max_index, min_index)
    pop2 = min(max_index, min_index)
    weekly_seasn.pop(pop1)
    weekly_seasn.pop(pop2)
    days_of_week.pop(pop1)
    days_of_week.pop(pop2)
    other_good_index = [indx for indx, i in enumerate(weekly_seasn) if i > .01]
    other_bad_index = [indx for indx, i in enumerate(weekly_seasn) if i < -.01]
    good_str, bad_str, other_str = \
        string_weekly_seasonality(
            max_index, min_index, other_good_index, other_bad_index)
    weekrec_list = []
    weekrec_list.append(good_str)
    weekrec_list.append(bad_str)
    weekrec_list.append(other_str)
    weekrec_output = "<br>".join(weekrec_list)
    return weekrec_output


def date_list_to_print(date_list, list_pct, better_worse):
    if len(date_list) == 0:
        outstring = \
            ["There aren't any dates for which similar bands book gigs \
             that are at least " + list_pct
             + " percent " + better_worse + " than average<br>"]
    else:
        outlist = []
        for item in date_list:
            outlist.append(item)
        outstring = ", ".join(outlist) + "<br>"
    return outstring


def get_best_dates(preds_df):
    future_preds = preds_df.loc[(preds_df['ds'] > dt.date(2018, 12, 13))]
    best_date = str(future_preds.nlargest(1, 'yhat').iloc[0]['ds'].date())
    worst_date = str(future_preds.nsmallest(1, 'yhat').iloc[0]['ds'].date())
    mean_pred_yhat = future_preds['yhat'].mean()
    best_date_pred = future_preds.nlargest(1, 'yhat').iloc[0]['yhat']
    best_date_pct = str(int((best_date_pred / mean_pred_yhat - 1) * 100))
    worst_date_pred = future_preds.nsmallest(1, 'yhat').iloc[0]['yhat']
    worst_date_pct = str(int(100 - (worst_date_pred / mean_pred_yhat) * 100))
    best_date_print = "The best possible date to play is <b>" \
        + best_date + "</b><br> (similar bands book gigs that are about " \
        + best_date_pct + " percent better than average on this date)<br>"
    worst_date_print = "The worst possible date to play is <b>" \
        + worst_date + "</b><br> (similar bands book gigs that are about" \
        + worst_date_pct + " percent worse than average on this date)<br>"
    good_10_pct = []
    bad_10_pct = []
    good_5_pct = []
    bad_5_pct = []
    for index, row in future_preds.iterrows():
        rowpct = future_preds['yhat'][index] / mean_pred_yhat
        if rowpct > 1.1:
            good_10_pct.append(str(future_preds['ds'][index].date()))
        elif rowpct > 1.05:
            good_5_pct.append(str(future_preds['ds'][index].date()))
        elif rowpct < .9:
            bad_10_pct.append(str(future_preds['ds'][index].date()))
        elif rowpct < .95:
            bad_5_pct.append(str(future_preds['ds'][index].date()))
    good_10_print = date_list_to_print(good_10_pct, '10', 'better')
    good_5_print = date_list_to_print(good_5_pct, '5', 'better')
    bad_10_print = date_list_to_print(bad_10_pct, '10', 'worse')
    bad_5_print = date_list_to_print(bad_5_pct, '5', 'worse')
    output = "<div class='rec-box' align='center'>"\
        + "<h3>Start here (the best dates):</h3>" \
        + good_10_print \
        + "</div>" \
        + "<div class='rec-box' align='center'>" \
        + "<h3>Try these next (pretty good dates):</h3>" \
        + good_5_print \
        + "</div>" \
        + "<div class='rec-box' align='center'>" \
        + "<h3>Definitely avoid these:</h3>" \
        + bad_10_print \
        + "</div>" \
        + "<div class='rec-box' align='center'>" \
        + "<h3>Avoid if you can:</h3>" \
        + bad_5_print \
        + "</div>" \
        + "<font size='+1'>" \
        + "<h2>Best and worst date</h2>" \
        + best_date_print + "<br>" + worst_date_print \
        + "</font>"
    return output
