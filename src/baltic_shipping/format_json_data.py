import os
import json
from io import StringIO
import csv
from datetime import datetime

def create_csv(report_data, headings, file_name):
    if report_data:
        right_now = datetime.utcnow()
        csv_filename = f"{file_name}_{right_now}.csv"
        csv_output = StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(headings)
        writer.writerow([])
        writer.writerows(report_data)
        
        with open(csv_filename, "w", newline="") as file:
            file.write(csv_output.getvalue())
        
        print(f"✅ CSV created successfully")

def update_csv(report_data):
    # Path to your existing CSV file
    csv_file = "baltic_shipping_details.csv"

    # Append new data to the CSV file
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(report_data)

    print("New rows added successfully!")

page_names = ['baltic_shipping_2001_2401']

def format_json_data(page_name):
    file_name = f'baltic_shipping/new_baltic_json_data/{page_name}.json'
    with open(file_name, 'r') as file:
        data = json.load(file)
        ships_data = [ship['data'] for ship in data['all_data']]
        headings = [(' '.join(head.split('_'))).capitalize() for head in ships_data[0].keys()]
        report_data = [list(ship.values()) for ship in ships_data]
        update_csv(report_data)
        print(f"✅ New Rows added successfully for {file_name}")
        # create_csv(report_data, headings, 'baltic_shipping_details')
        

def format_engine_types():
    file_name = 'baltic_shipping/baltic_json_data/baltic_engine_types.json'
    with open(file_name, 'r') as file:
        data = json.load(file)
        engine_data = data['engine_types']
        headings = [(' '.join(head.split('_'))).capitalize() for head in  engine_data[0].keys()]
        report_data = [list(ship.values()) for ship in engine_data]
        create_csv(report_data, headings, 'baltic_engine_types')

def get_all_file_names():
    folder_path = "baltic_shipping/baltic_json_data"
    files = os.listdir(folder_path)  # List of file names
    files = [file.split('.')[0] for file in files]
    return files

def extract_previous_year_searoute_imos():
    csv_file = "last_year_sailed_vessels.csv"
    imo_list = []
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            if row[0]:
                imo_list.append(int(row[0]))

    return imo_list

def extract_all_cogoport_imos():
    csv_file = "all_cogoport_vessels.csv"
    imo_list = []
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[1]:
                imo_list.append(int(row[1]))

    return imo_list

def extract_all_baltic_imos():
    csv_file = "baltic_shipping_details.csv"
    imo_list = []
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        print("Header:", header)
        for row in reader:
            breakpoint()
            if row[0]:
                imo_list.append(int(row[0]))

    return imo_list

def combine_all_baltic_json():
    filename = 'baltic_json_combine.json'
    filenames = get_all_file_names()
    combine_json_data = []
    for file in filenames:
        file_path = f'baltic_shipping/baltic_json_data/{file}.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
            combine_json_data.extend(data['all_data'])
    
    with open(filename, "w") as file:
        json.dump(combine_json_data, file, indent=4)
    
    return filename