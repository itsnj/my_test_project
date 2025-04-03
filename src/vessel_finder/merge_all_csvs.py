import csv
import glob
import os

def get_all_file_names():
    folder_path = "vessel_finder/vessel_finder_csvs"
    files = os.listdir(folder_path)  # List of file names
    # files = [file.split('.')[0] for file in files]
    return files

def merge_csvs(csv_files):
    output_file = "merged_output.csv"

    # Read and merge CSV files
    with open(output_file, "w", newline="") as outfile:
        writer = None  # Will initialize after reading headers once
        for i, file in enumerate(csv_files):
            file_path = f"vessel_finder/vessel_finder_csvs/{file}"
            with open(file_path, "r", newline="") as infile:
                reader = csv.reader(infile)
                headers = next(reader)  # Read header from each file
                
                # Write header only once (from the first file)
                if i == 0:
                    writer = csv.writer(outfile)
                    writer.writerow(headers)

                # Write remaining rows
                for row in reader:
                    writer.writerow(row)

    print(f"Merged {len(csv_files)} CSV files into {output_file}")