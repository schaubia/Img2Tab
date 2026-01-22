# Table Screenshot to Excel/CSV Converter

A free Streamlit application that converts screenshots of tables into downloadable CSV or XLSX files using OCR (Optical Character Recognition).

## Features

- 📸 Upload JPG or PNG images containing tables
- 🔧 **Advanced image preprocessing** for better OCR accuracy:
  - Contrast enhancement
  - Edge sharpening
  - Noise reduction
  - Binarization (black & white conversion)
- 🔍 Automatic text extraction using Tesseract OCR
- 📊 Convert extracted data to structured DataFrame
- 🎛️ Toggle header row recognition
- 👀 Side-by-side preview of original and processed images
- 💾 Download as CSV or XLSX format
- 🎯 Automatic numeric data type detection

## Installation & Setup

### Prerequisites

You need to install Tesseract OCR on your system:

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**On macOS:**
```bash
brew install tesseract
```

**On Windows:**
- Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
- Add Tesseract to your PATH

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deploying to Streamlit Cloud (FREE)

1. **Create a GitHub Repository:**
   - Create a new repository on GitHub
   - Upload `app.py` and `requirements.txt`

2. **Add packages.txt for Tesseract:**
   Create a file named `packages.txt` in your repository with:
   ```
   tesseract-ocr
   tesseract-ocr-eng
   ```

3. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

Your app will be live at a free Streamlit Cloud URL!

## Usage

1. Click "Browse files" to upload a screenshot (JPG or PNG)
2. **Adjust preprocessing settings** in the sidebar:
   - Enable "Enhance Contrast" for better visibility
   - Enable "Sharpen Edges" to make borders clearer
   - Enable "Reduce Noise" to clean up the image
   - Enable "Binarize" for tables with very clear borders (black & white)
3. View the original and processed images side-by-side
4. Check or uncheck "Table has a header row" as needed
5. Review the extracted table data
6. Click "Download as CSV" or "Download as XLSX"
7. Check the "Raw Extracted Text" expander to see what OCR detected

## Tips for Best Results

- **Start with default preprocessing settings** - they work well for most tables
- **For low-contrast images**: Enable all preprocessing options
- **For very clear tables**: Try enabling "Binarize" for best results
- **If text is blurry**: Make sure "Sharpen Edges" is enabled
- **If background is noisy**: Enable "Reduce Noise"
- Use high-resolution images with clear, readable text
- Ensure good contrast between table text and background
- Tables with clear column alignment work best
- Avoid skewed or rotated images
- Make sure the table has distinct row/column structure

## How It Works

1. **Image Upload**: User uploads a JPG/PNG screenshot
2. **Preprocessing**: Image is enhanced based on selected options:
   - Contrast is increased to make text/borders more visible
   - Edges are sharpened to enhance table borders
   - Noise is reduced for cleaner OCR
   - Optional binarization for maximum clarity
3. **OCR Processing**: Tesseract extracts text from the processed image
4. **Table Parsing**: Text is parsed into rows and columns
5. **Data Cleaning**: Numeric values are detected and converted
6. **DataFrame Creation**: Data is structured in a pandas DataFrame
7. **Export**: User can download as CSV or XLSX

## Limitations

- OCR accuracy depends on image quality
- Complex tables with merged cells may not parse correctly
- Handwritten tables won't work well
- Very large tables may need manual review

## Technologies Used

- **Streamlit**: Web application framework
- **Pytesseract**: Python wrapper for Tesseract OCR
- **Pandas**: Data manipulation and analysis
- **Pillow**: Image processing
- **OpenPyXL**: Excel file creation

## License

Free to use and modify for personal and commercial projects.

## Troubleshooting

**"TesseractNotFoundError":**
- Make sure Tesseract is installed on your system
- On Windows, add Tesseract to PATH or set the path in code:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

**Poor OCR results:**
- Try different preprocessing combinations
- Enable "Binarize" for tables with clear borders
- Increase image resolution before uploading
- Improve image contrast using the preprocessing options
- Ensure text is horizontal and not rotated
- Use simpler fonts if possible

**Table not parsing correctly:**
- The app assumes columns are separated by multiple spaces
- Try enabling "Sharpen Edges" to make borders more distinct
- Check if the processed image preview shows clear separation
- Manual adjustment of the parsing logic may be needed for specific table formats
