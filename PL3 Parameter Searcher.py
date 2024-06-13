import os
import tkinter as tk
from tkinter import filedialog
import logging

# ログの設定（エンコーディングを utf-8 に設定）
logging.basicConfig(filename='PL3_Parameter_Searcher.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# 検索するパラメータとその値
voltages = ["40", "60", "80", "100"]
flow_rates = ["2", "5", "8"]
distances = ["0", "30", "50", "100", "140", "140_2"]

def search_parameters_in_files(directory, voltages, flow_rates, distances):
    results = {}
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".pl3"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            matches = search_file_data(file_data, voltages, flow_rates, distances)
                            if matches:
                                results[file_path] = matches
                                logging.info(f"File {file_path} matches found: {matches}")
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {e}")
                        print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        logging.error(f"Error walking directory {directory}: {e}")
        print(f"Error walking directory {directory}: {e}")
    
    return results

def search_file_data(file_data, voltages, flow_rates, distances):
    matches = {}
    for voltage in voltages:
        for flow_rate in flow_rates:
            for distance in distances:
                search_strings = [
                    f'V={voltage}\\F={flow_rate}\\x2={distance}\\',
                    f'V={voltage}\\F={flow_rate}\\x0={distance}\\'
                ]
                for search_string in search_strings:
                    count = file_data.count(search_string.encode())
                    if count > 0:
                        matches[search_string] = matches.get(search_string, 0) + count
    return matches

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        process_directory(directory)

def process_directory(directory):
    try:
        logging.info(f"Selected directory: {directory}")
        matching_files = search_parameters_in_files(directory, voltages, flow_rates, distances)
        display_results(matching_files)
    except Exception as e:
        logging.error(f"Error processing directory {directory}: {e}")
        print(f"Error processing directory {directory}: {e}")

def display_results(matching_files):
    if matching_files:
        print("指定したパラメータが含まれているファイル:")
        for file, params in matching_files.items():
            print(f"ファイル: {file} に以下のパラメータが含まれています:")
            for param, count in params.items():
                print(f"  - {param} : {count}回")
    else:
        print("指定したパラメータが含まれているファイルは見つかりませんでした。")
    logging.info("Search completed.")

# GUIの設定
root = tk.Tk()
root.title("PL3 Parameter Searcher")

label = tk.Label(root, text="ディレクトリを選択してください。")
label.pack(pady=10)

select_button = tk.Button(root, text="ディレクトリを選択", command=select_directory)
select_button.pack(pady=5)

root.mainloop()
