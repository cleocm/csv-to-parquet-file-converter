import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import sys
import os

def csv_to_parquet(csv_filename, parquet_filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_filename)
    
    # Convert the DataFrame into an Arrow Table
    table = pa.Table.from_pandas(df)
    
    # Write the Table to a Parquet file
    pq.write_table(table, parquet_filename)

def generate_unique_filename(base_filename, extension):
    """
    Generate a unique filename by adding (1), (2), etc., if the file already exists.
    """
    filename = base_filename + extension
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}({counter}){extension}"
        counter += 1
    return filename


if __name__ == "__main__":
    # Get the CSV filename from the command line arguments
    csv_file = sys.argv[1]
    
    # Set the Parquet filename (save it in the same directory as the CSV file)
    base_parquet_file = os.path.splitext(csv_file)[0]

    # Generate a unique Parquet filename
    parquet_file = generate_unique_filename(base_parquet_file, ".parquet")
    
    # Ensure that the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file {csv_file} not found.")
        sys.exit(1)
    
    # Call the conversion function
    csv_to_parquet(csv_file, parquet_file)
    
    # Return the Parquet file path to PHP (this prints to stdout)
    print(parquet_file)
