"""
Sample script to test the OCR table extraction locally
This can be used to test the core functionality without running Streamlit
"""

from PIL import Image
import pytesseract
import pandas as pd
import re

def extract_table_from_image(image_path):
    """Extract table data from an image file"""
    
    # Load image
    image = Image.open(image_path)
    
    # Extract text using Tesseract
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(image, config=custom_config)
    
    print("Raw extracted text:")
    print(extracted_text)
    print("\n" + "="*50 + "\n")
    
    # Parse text into table
    lines = extracted_text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    table_data = []
    for line in lines:
        # Split by multiple spaces or tabs
        row = re.split(r'\s{2,}|\t+', line)
        row = [cell.strip() for cell in row if cell.strip()]
        if row:
            table_data.append(row)
    
    if not table_data:
        print("No table data found!")
        return None
    
    # Determine max columns
    max_cols = max(len(row) for row in table_data)
    
    # Pad rows
    for row in table_data:
        while len(row) < max_cols:
            row.append('')
    
    # Create DataFrame
    if len(table_data) > 1:
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
    else:
        df = pd.DataFrame(table_data)
    
    # Convert numeric columns
    for col in df.columns:
        try:
            df[col] = df[col].str.replace(',', '').str.replace('$', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    return df

if __name__ == "__main__":
    # Test with your image
    image_path = "test_table.png"  # Replace with your image path
    
    try:
        df = extract_table_from_image(image_path)
        
        if df is not None:
            print("Extracted DataFrame:")
            print(df)
            print("\n" + "="*50 + "\n")
            
            # Save to CSV
            df.to_csv("output.csv", index=False)
            print("Saved to output.csv")
            
            # Save to Excel
            df.to_excel("output.xlsx", index=False)
            print("Saved to output.xlsx")
    except FileNotFoundError:
        print(f"Error: Could not find image file '{image_path}'")
        print("Please update the image_path variable with your test image.")
    except Exception as e:
        print(f"Error: {e}")
