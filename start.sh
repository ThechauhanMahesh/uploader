echo "Starting aria2c"
tracker_list=$(curl -Ns https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt | awk '$0' | tr '\n\n' ',')
aria2c --enable-rpc \
          --rpc-listen-all=false \
          --rpc-listen-port=6800 \
          --max-connection-per-server=10 \
          --rpc-max-request-size=1024M \
          --check-certificate=false \
          --follow-torrent=mem \
          --seed-time=0 \
          --max-upload-limit=1K \
          --max-concurrent-downloads=5 \
          --min-split-size=10M \
          --follow-torrent=mem \
          --split=10 \
          --bt-tracker="[$tracker_list]" \
          --daemon=true \
          --allow-overwrite=true
          
echo "Running main"
python3 -m main
