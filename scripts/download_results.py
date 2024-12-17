from os import mkdir
import pandas as pd
import gdown
def download_google_drive_file(drive_url, output_filename=None):
    """
    Downloads a file from a Google Drive link using gdown.
    :param drive_url: str, the Google Drive link
    :param output_filename: str, optional, the desired name of the downloaded file
    :return: str, the path to the downloaded file
    """
    try:
        # Extract the file ID from the URL
        if 'drive.google.com' in drive_url:
            if '/file/d/' in drive_url:
                file_id = drive_url.split('/d/')[1].split('/')[0]
            elif 'id=' in drive_url:
                file_id = drive_url.split('id=')[1].split('&')[0]
            else:
                raise ValueError("Invalid Google Drive URL format.")
            download_url = f"https://drive.google.com/uc?id={file_id}"
            # If no output filename is provided, use the file ID
            if not output_filename:
                output_filename = f"{file_id}.file"
            # Download the file
            gdown.download(download_url, output_filename, quiet=False)
            return output_filename
        else:
            raise ValueError("The URL provided is not a Google Drive link.")
    except Exception as e:
        print(f"Failed to download the file from {drive_url}: {e}")
        return None
def download_files_from_csv(csv_file_path):
    """
    Reads a CSV file and downloads files from Google Drive links in the 'Results File' column,
    saving them with filenames based on the 'Job Number' column.
    :param csv_file_path: str, path to the CSV file
    """
    output_folder = csv_file_path.split('.')[0]
    mkdir(output_folder)
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            drive_url = row.get('Results File')
            job_number = row.get('Job Number')
            # Skip if either field is missing
            if pd.isnull(drive_url) or pd.isnull(job_number):
                print(f"Row {index} missing 'Results File' or 'Job Number'. Skipping.")
                continue
            # Construct the output filename using the job number
            output_filename = f"{output_folder}/{job_number.split('.')[0]}_results.json"
            # Download the file
            result = download_google_drive_file(drive_url, output_filename)
            if result:
                print(f"Downloaded {output_filename} from {drive_url}")
            else:
                print(f"Failed to download file for job number {job_number}")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

if __name__ == "__main__":
    # Replace with your actual CSV file path
    csv_file_path = 'aquila_jobs_28_11_2024.csv'
    download_files_from_csv(csv_file_path)
