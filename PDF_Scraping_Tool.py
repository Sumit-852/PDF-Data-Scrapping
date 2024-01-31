import os
import re
import pdfplumber
import pandas as pd
import time


pdf_directory = '' #Add dir path of invocices here
csv_file_path = '' #Output file path
data = []

# Start the timer
start_time = time.time()

# Iterate over the PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        filepath = os.path.join(pdf_directory, filename)
        print(filepath)
        try:
            with pdfplumber.open(filepath) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()

                p_invoice_number = re.compile("Invoice Number: (\w+)")
                invoice_number = p_invoice_number.search(text).group(1)

                p_internet = re.compile("^(?:[^\n]*\n){1}([^\n]*) (.*)Internet")
                internet = p_internet.search(text).group(1)

                p_invoice_period = re.compile("Invoice Period: (\w+ 2019)")
                invoice_period = p_invoice_period.search(text).group(1)

                p_request_price = re.compile(r"Request Price\n([\s\S]*?)TOTAL USD", re.MULTILINE)
                request_price_lines = p_request_price.search(text).group(1).split("\n")
                request_price = "\n".join(request_price_lines)

                # Append the extracted data to the list
                data.append({
                    'Invoice Number': invoice_number,
                    'Internet': internet,
                    'Invoice Period': invoice_period,
                    'Request Price': request_price
                })
        except Exception as e:
            print(f"Error processing file: {filename}. Error message: {str(e)}")

# Calculate the elapsed time
elapsed_time = time.time() - start_time

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

# Print the elapsed time
print(f"Time taken: {elapsed_time} seconds")