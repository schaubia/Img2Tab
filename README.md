# Table Screenshot to Excel/CSV Converter

A free Streamlit application that converts screenshots of tables into downloadable CSV or XLSX files using OCR (Optical Character Recognition).

## Features

- 📸 Upload JPG or PNG images containing tables
- 📋 **Paste images directly from clipboard** - quick screenshot workflow
- 🎚️ **Advanced image preprocessing with granular slider controls**:
  - Adjustable contrast enhancement (0.0 - 3.0x)
  - Adjustable sharpness (0.0 - 3.0x)
  - Adjustable brightness (0.5 - 2.0x)
  - Noise reduction toggle
  - Binarization with adjustable threshold (0-255)
  - Quick presets for common scenarios
- 🔍 Automatic text extraction using Tesseract OCR
- 📊 Convert extracted data to structured DataFrame
- 🎛️ Toggle header row recognition
- 🔢 **Column count hint** - specify expected number of columns for improved parsing
- 👀 Side-by-side preview of original and processed images with real-time updates
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

1. **Choose input method** - use either tab:
   - **Upload File**: Click "Browse files" to upload a screenshot (JPG or PNG)
   - **Paste from Clipboard**: 
     - Take a screenshot (Windows: Win+Shift+S, Mac: Cmd+Shift+4)
     - Click the paste button and press Ctrl+V (or Cmd+V on Mac)
2. **Adjust preprocessing sliders** in the sidebar for optimal results:
   - **Contrast Enhancement**: Drag slider to adjust contrast (default: 2.0x)
   - **Sharpness**: Control edge sharpness (default: 1.5x)
   - **Brightness**: Adjust overall brightness (default: 1.0x)
   - **Reduce Noise**: Toggle to remove artifacts
   - **Binarize**: Enable for black & white conversion
   - **Binarization Threshold**: Fine-tune the black/white cutoff (only when binarize enabled)
   - **Quick Presets**: Click "Clear Table" or "Low Quality" for instant optimal settings
3. View the original and processed images side-by-side with real-time updates
4. Check or uncheck "Table has a header row" as needed
5. **Optional:** Enable "Specify number of columns" and enter the exact column count if you know it
   - This can help improve parsing for tables with known column counts
   - The tool will attempt to split or merge data to match your specified columns
6. Review the extracted table data
7. Click "Download as CSV" or "Download as XLSX"
8. Check the "Raw Extracted Text" expander to see what OCR detected

## Tips for Best Results

- **Use clipboard paste for quick workflow** - take a screenshot and paste directly!
- **Start with default slider settings** - they work well for most tables
- **Use Quick Presets**:
  - "Clear Table" - for high-quality scans with clear borders
  - "Low Quality" - for blurry, low-contrast, or poorly lit images
- **To reset**: Simply refresh the page or re-upload your image
- **Fine-tune individual sliders**:
  - **Contrast too low?** → Text appears faint → Increase contrast slider
  - **Contrast too high?** → Text bleeds together → Decrease contrast slider
  - **Blurry borders?** → Increase sharpness slider
  - **Image too dark/light?** → Adjust brightness slider
  - **For binarization**: Lower threshold = more black, Higher threshold = more white
- **Use "Specify number of columns"** if you know your table's exact column count
- **Watch the processed image preview** - adjust sliders until table borders and text are clearly visible
- Use high-resolution images with clear, readable text
- Tables with clear column alignment work best
- Avoid skewed or rotated images

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
