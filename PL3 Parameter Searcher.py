import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import logging

# ログの設定
logging.basicConfig(filename='PL3_Parameter_Searcher.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 検索するパラメータとその値
voltages = ["40", "60", "80", "100"]
flow_rates = ["2", "5", "8"]
distances = ["0", "30", "50", "100", "140", "なし"]

def search_parameters_in_files(directory, voltages, flow_rates, distances):
    results = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pl3"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                        matches = []
                        for voltage in voltages:
                            for flow_rate in flow_rates:
                                for distance in distances:
                                    search_string = f'V={voltage}\\F={flow_rate}\\x2={distance}\\'
                                    if search_string.encode() in file_data:
                                        matches.append(search_string)
                        if matches:
                            results[file_path] = matches
                            logging.info(f"File {file_path} matches found: {matches}")
                except Exception as e:
                    logging.error(f"Error reading file {file_path}: {e}")
    
    return results

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        process_directory(directory)

def enter_directory():
    directory = simpledialog.askstring("Input", "ディレクトリのパスを入力してください:")
    if directory:
        process_directory(directory)

def process_directory(directory):
    logging.info(f"Selected directory: {directory}")
    matching_files = search_parameters_in_files(directory, voltages, flow_rates, distances)
    if matching_files:
        print("指定したパラメータが含まれているファイル:")
        for file, params in matching_files.items():
            print(f"ファイル: {file} に以下のパラメータが含まれています:")
            for param in params:
                print(f"  - {param}")
    else:
        print("指定したパラメータが含まれているファイルは見つかりませんでした。")
    logging.info("Search completed.")

# GUIの設定
root = tk.Tk()
root.title("PL3 Parameter Searcher")

label = tk.Label(root, text="ディレクトリの選択方法を選んでください。")
label.pack(pady=10)

select_button = tk.Button(root, text="GUIでディレクトリを選択", command=select_directory)
select_button.pack(pady=5)

enter_button = tk.Button(root, text="文字列でディレクトリを入力", command=enter_directory)
enter_button.pack(pady=5)

root.mainloop()