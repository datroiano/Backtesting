import pandas as pd
import os


def save_df_to_excel(df: pd.DataFrame, file_name: str = 'data.xlsx') -> None:
    """
    Save a pandas DataFrame to an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        file_name (str): The name of the Excel file to be created.

    Returns:
        None
    """
    try:
        # Get the user's download folder path
        download_folder = os.path.expanduser("~\\Downloads\\")
        file_path = os.path.join(download_folder, file_name)

        # Write DataFrame to Excel with adjusted column widths
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            worksheet = writer.sheets['Sheet1']  # Assuming the sheet name is Sheet1

            # Adjust column widths based on the maximum width of the data in each column
            for i, col in enumerate(df.columns):
                max_width = max(df[col].astype(str).map(len).max(), len(col)) + 0.02  # Add extra padding
                worksheet.set_column(i, i, max_width)
    except PermissionError:
        print("Permission Error. Check file status.")
