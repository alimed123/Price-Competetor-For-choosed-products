import csv
import sys
import threading
import concurrent.futures
import pandas as pd
import time
import os

def process_row(row):
  # Simulate processing by printing the row
  print("Processing:", row[0])

def process_csv(filename, num_threads):
  with open(filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Skip the header

    # Create a ThreadPoolExecutor with a maximum of num_threads workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
      # Submit tasks for each row
      futures = [executor.submit(process_row, row) for row in csv_reader]

      # Wait for all tasks to complete
      concurrent.futures.wait(futures)

if __name__ == "__main__":
  directory = os.path.dirname(os.path.realpath(__file__))
  filename = f'{directory}/multitheading_test_input.csv'
  num_threads = 10  # Adjust as needed

  process_csv(filename, num_threads)