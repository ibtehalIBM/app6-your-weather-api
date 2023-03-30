from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data_small/stations.txt', skiprows=17)
df = df[['STAID', 'STANAME                                 ']]


@app.route('/')
def home():
    return render_template('home.html', data=df.to_html())


@app.route('/api/v1/<station>/<date>')
def get_temperature(station, date):
    station_file_name = 'TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(f'data_small/{station_file_name}', skiprows=20, parse_dates=['   DATE'])
    temperature = df.loc[df['   DATE'] == date]['   TG'].squeeze() / 10
    return {'date': date,
            'station': station_file_name,
            'temperature': temperature}


@app.route('/api/v1/<station>')
def get_all_stations(station):
    station_file_name = 'TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(f'data_small/{station_file_name}', skiprows=20, parse_dates=['   DATE'])
    result = df.to_dict(orient='records')
    return result


@app.route('/api/v1/yearly/<station>/<year>')
def yearly(station, year):
    station_file_name = 'TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(f'data_small/{station_file_name}', skiprows=20)
    df['   DATE'] = df['   DATE'].astype(str)
    df = df.loc[df['   DATE'].str.startswith(str(year))]
    result = df.to_dict(orient='records')
    return result


if __name__ == '__main__':
    app.run(debug=True)
