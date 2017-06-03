# Stats-Analytics

Collects automatically daily stats (users, pageviews...) from Google Analytics monitored websites and version results in [`data`](data).

- [RegardsCitoyens.org](https://github.com/regardscitoyens/stats-analytics/raw/master/data/RegardsCitoyens.org.csv)
- [NosDéputés.fr](https://github.com/regardscitoyens/stats-analytics/raw/master/data/NosD%E9put%E9s.fr.csv)
- [NosSénateurs.fr](https://github.com/regardscitoyens/stats-analytics/raw/master/data/NosS%E9nateurs.fr.csv)

Data is redistributed as OpenData under ([ODbL licence](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode)).

## Install

- Create a virtualenv `analytics` using `virtualenvwrapper` and install dependencies:

```bash
sudo apt-get install virtualenvwrapper
source $(which virtualenvwrapper.sh)
mkvirtualenv analytics
pip install -r requirements.txt
```

- Or install dependency library globally:

```bash
sudo pip install google-api-python-client
```

## Configure

- Create a new project in the [Google API Console](https://console.developers.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key) and create a service account. This will let you download a json file with credentials.

- Move this file to the current directory and rename it `ga-pi-credentials.json`. It should look similar to [`ga-api-credentials.json.example`](ga-api-credentials.json.example).

- In the Google API Console, click on the newly created accound to read its details and copy its e-mail address. Then connect to [Google Analytics Admin Seettings](https://analytics.google.com/analytics/web/#management/Settings/) and add a user with this e-mail and "Read & Analyze" permissions.

- Copy [`settings.py.example`](settings.py.example) and edit it to setup chosen websites (`VIEWS`) and resulting data (`FIELDS`).

```bash
cp settings.py{.example,}
```

## Run

- Collect all data

```bash
./collect.py
```

- Book automatic git versioning of data with `update.sh` and a cronjob.

```
./update.sh
```

Crontab:

```crontab
m  h  dom mon dow   command
5  3   *   *   *    $PATH_TO_THIS_REPO/update.sh 2>&1
```
