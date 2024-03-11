import json
import time
from sensorstream import plot_data, plot_init

# 
# Execute this recipe by: 
#   streamlit run --server.port 9947 ttn_fake.py
#

fname = 'synth_beacons.json'

beacon_data = {}

# Acquires upstream messages from device
def process_message(dev_eui, records):
    global beacon_data
    signal_dict = {}

    for record in records:
        if record['ble_id'] == 'wand':
            signal_dict['wand'] = {
                "latitude":record['latitude'],
                "longitude":record['longitude'],
                }
        else:
            signal_dict[record['ble_id']] = round(100+record['ble_rssi'],2)
    beacon_data[dev_eui] = signal_dict

if __name__ == "__main__":
    # and listen to server
    fjson = open(fname,'r')
    reports = json.load( fjson )
    plot_init()
    time0 = reports[0]['time']
    records = []
    while True:
        for report in reports:
            if report['time'] == time0:
                records.append(report)
            else:
                process_message('deadbeef00000006', records)
                plot_data( beacon_data )
                time0 = report['time']
                records=[]
                records.append(report)
            time.sleep(0.3)
        print("Done")

