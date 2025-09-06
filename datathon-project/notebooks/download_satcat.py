import configparser
from spacetrack import SpaceTrackClient
import json
import time

#the credintials file can be created using notepad saved as .ini. Type your username and password that you used to create an account in Space-track in notepad and save as .ini
# Read credentials from the configuration file
config = configparser.ConfigParser()
config.read('D:/DATA/config.ini')

try:
    username = config['space-track']['username']
    password = config['space-track']['password']
except KeyError:
    print("Error: Make sure your config.ini file has a [space-track] section with 'username' and 'password'.")
    exit()

# List of country codes to filter by
country_codes = ['US', 'CA', 'PRC', ]

try:
    # Initialize the SpaceTrackClient
    st = SpaceTrackClient(identity=username, password=password)

    # 1. Download and filter the SATCAT data
    print(f"Downloading SATCAT data for countries: {', '.join(country_codes)}...")
    satcat_response = st.satcat(country=country_codes, orderby='NORAD_CAT_ID asc', format='json')

    if not satcat_response:
        print("No satellite data returned from the server for the specified countries.")
        exit()

    satcat_data = json.loads(satcat_response)
    print(f"Successfully found {len(satcat_data)} satellites.")

    # 2. Extract NORAD IDs from the downloaded data
    norad_ids = [satellite['NORAD_CAT_ID'] for satellite in satcat_data]
    print(f"Extracting {len(norad_ids)} NORAD IDs to fetch TLEs...")

    # 3. Download TLEs in batches
    all_tle_data = []
    chunk_size = 600
    num_batches = (len(norad_ids) + chunk_size - 1) // chunk_size

    print(f"Downloading latest TLE data in {num_batches} batches...")
    for i in range(0, len(norad_ids), chunk_size):
        batch_num = (i // chunk_size) + 1
        print(f"  - Fetching batch {batch_num} of {num_batches}...")
        batch_ids = norad_ids[i:i + chunk_size]
        
        tle_data_response = st.tle_latest(norad_cat_id=batch_ids, orderby='ORDINAL asc', format='json')

        if tle_data_response:
            batch_tle_data = json.loads(tle_data_response)
            if isinstance(batch_tle_data, dict):
                batch_tle_data = [batch_tle_data]
            all_tle_data.extend(batch_tle_data)
        
        time.sleep(1)

    if not all_tle_data:
        print("Could not retrieve any TLE data for the found satellites.")
        exit()

    print(f"Successfully downloaded {len(all_tle_data)} TLE records.")

    # 4. Correctly assemble TLE pairs from the records
    print("Assembling TLE pairs...")
    tles_by_norad_id = {}
    malformed_records = 0

    for tle_record in all_tle_data:
        if 'NORAD_CAT_ID' not in tle_record:
            malformed_records += 1
            continue

        norad_id = tle_record['NORAD_CAT_ID']

        if norad_id not in tles_by_norad_id:
            tles_by_norad_id[norad_id] = {'OBJECT_NAME': tle_record.get('OBJECT_NAME', 'N/A')}

        if tle_record.get('TLE_LINE1'):
            tles_by_norad_id[norad_id]['TLE_LINE1'] = tle_record['TLE_LINE1']
        
        if tle_record.get('TLE_LINE2'):
            tles_by_norad_id[norad_id]['TLE_LINE2'] = tle_record['TLE_LINE2']

    if malformed_records > 0:
        print(f"Warning: Skipped {malformed_records} malformed records that were missing a NORAD_CAT_ID.")

    # 5. Prepare the final combined data structure
    final_data = []
    for satellite in satcat_data:
        norad_id = satellite['NORAD_CAT_ID']
        tle_info = tles_by_norad_id.get(norad_id)

        # Create a dictionary for each satellite
        satellite_entry = {
            "OBJECT_NAME": satellite.get('OBJECT_NAME'),
            "NORAD_CAT_ID": norad_id,
            "INTLDES": satellite.get('INTLDES'),
            "COUNTRY": satellite.get('COUNTRY'),
            "LAUNCH_DATE": satellite.get('LAUNCH'),
            "TLE_DATA": None # Default to None if no TLE is found
        }
        
        # If a complete TLE was found, add it
        if tle_info and 'TLE_LINE1' in tle_info and 'TLE_LINE2' in tle_info:
            satellite_entry["TLE_DATA"] = {
                "TLE_OBJECT_NAME": tle_info.get('OBJECT_NAME'),
                "TLE_LINE1": tle_info.get('TLE_LINE1'),
                "TLE_LINE2": tle_info.get('TLE_LINE2'),
            }
        
        final_data.append(satellite_entry)

    # 6. Save the final data to a JSON file
    file_name = 'D:/DATA/satellite_data1.json'
    print(f"\nSaving all combined data to '{file_name}'...")
    with open(file_name, 'w') as json_file:
        json.dump(final_data, json_file, indent=2)

    print(f"Successfully saved data for {len(final_data)} satellites.")
    print("Script finished.")


except Exception as e:
    print(f"An error occurred: {e}")