import random
from datetime import date, datetime, time, timedelta

import numpy
from flask import Flask, render_template, request

activities = [
    'finish marketing content',
    'accounting',
    'website/social media changes',
    'research',
    'design collateral',
    'complete project',
    'data analysis',
]

weights = [
    0.20,
    0.05,
    0.25,
    0.10,
    0.25,
    0.05,
    0.10,
]

app = Flask(__name__)


@app.route('/')
def home():
    year = int(request.args.get('year', 2016))
    num_entries = int(request.args.get('entries', 100))
    start_date = date(month=1, day=1, year=year).toordinal()
    end_date = date(month=12, day=31, year=year).toordinal()
    dates = [date.fromordinal(random.randint(start_date, end_date)) for _ in range(num_entries)]
    dates.sort()
    reasons = numpy.random.choice(activities, num_entries, p=weights)
    entries = [{'date': dates[i], 'reason': reasons[i], 'is_weekday': dates[i].weekday() <= 4} for i in
               range(num_entries)]
    for entry in entries:
        start_minute = random.randint(0, 59)
        if entry['is_weekday']:
            start_hour = random.randint(19, 21)
            if start_hour == 21 and start_minute > 0:
                start_hour -= 1
            duration_in_minutes = random.randint(3 * 60, 4 * 60)
        else:
            start_hour = random.randint(7, 20)
            if start_hour == 20 and start_minute > 0:
                start_hour -= 1
            duration_in_minutes = random.randint(4 * 60, 5 * 60)

        start_time = time(hour=start_hour, minute=start_minute)
        duration = timedelta(minutes=duration_in_minutes)
        end_time = (datetime.combine(entry['date'], start_time) + duration).time()

        entry['start_time'] = start_time
        entry['end_time'] = end_time

    return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    # Use this port=33507 when you want to Flask to work on Heroku....
    app.run()
