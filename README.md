# Stats-Analytics

Pour chaque site voulu :
- sélectionner la période souhaitée (début ND : 2009-09-14, début NS : 2011-09-22)
- sélectionner dans l'onglet Overview "Users VS. Pageviews"
- cliquer sur Export
- faire tourner le script de reformatage sur le fichier téléchargé, par exemple :
```bash
./reformat_analytics_csv.py Analytics\ www.nosdeputes.fr\ Audience\ Overview\ 20090914-20170513.csv > NosDéputés.fr-20090914-20170513.csv
```
