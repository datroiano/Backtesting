from TestCases.straddle_runner import learning_frame
import os


df = learning_frame

download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Writing DataFrame to CSV
csv_file_path = os.path.join(download_folder, "simulated_trades.csv")
df.to_csv(csv_file_path, index=False)

print(f"CSV file saved to: {csv_file_path}")


