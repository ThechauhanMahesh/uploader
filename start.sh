echo "Adding files required for aria2 config"
wget -O /app/dht.dat https://github.com/P3TERX/aria2.conf/raw/master/dht.dat 
wget -O /app/dht6.dat https://github.com/P3TERX/aria2.conf/raw/master/dht6.dat 
TRACKER=`curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt -: https://ngosang.github.io/trackerslist/trackers_all_http.txt -: https://newtrackon.com/api/all -: https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt -: https://torrends.to/torrent-tracker-list/?download=latest | awk '$1' | tr '\n' ',' | cat`
ran=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)

echo "Running main"
python3 -m main
