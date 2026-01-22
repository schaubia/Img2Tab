import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import io
import re
import numpy as np

st.set_page_config(page_title="Table Screenshot to Excel/CSV", page_icon="📊", layout="wide")

def preprocess_image(image, enhance_contrast=True, sharpen=True, denoise=True, binarize=False):
    """
    Preprocess image to improve OCR accuracy
    """
    processed = image.copy()
    
    # Convert to grayscale if needed
    if processed.mode != 'L' and processed.mode != 'RGB':
        processed = processed.convert('RGB')
    
    # Denoise
    if denoise:
        processed = processed.filter(ImageFilter.MedianFilter(size=3))
    
    # Enhance contrast
    if enhance_contrast:
        enhancer = ImageEnhance.Contrast(processed)
        processed = enhancer.enhance(2.0)  # Increase contrast
    
    # Sharpen edges (helps with borders)
    if sharpen:
        processed = processed.filter(ImageFilter.SHARPEN)
        processed = processed.filter(ImageFilter.EDGE_ENHANCE)
    
    # Binarize (convert to pure black and white)
    if binarize:
        processed = processed.convert('L')
        processed = ImageOps.autocontrast(processed)
        # Apply threshold
        threshold = 128
        processed = processed.point(lambda p: 255 if p > threshold else 0)
    
    return processed

st.title("📊 Table Screenshot Converter")
st.markdown("Upload a screenshot of a table, and I'll convert it to CSV or XLSX format")

uploaded_file = st.file_uploader("Choose an image file (JPG or PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Preprocessing options in sidebar
    st.sidebar.subheader("🔧 Image Preprocessing")
    st.sidebar.markdown("Enhance image quality for better OCR results")
    
    enhance_contrast = st.sidebar.checkbox("Enhance Contrast", value=True, 
                                          help="Increases contrast to make text and borders more visible")
    sharpen = st.sidebar.checkbox("Sharpen Edges", value=True,
                                  help="Sharpens borders and text edges")
    denoise = st.sidebar.checkbox("Reduce Noise", value=True,
                                  help="Removes noise and artifacts from the image")
    binarize = st.sidebar.checkbox("Binarize (Black & White)", value=False,
                                   help="Convert to pure black and white - best for clear tables")
    
    st.sidebar.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        # Ask if table has header row
        has_header = st.checkbox("Table has a header row", value=True, 
                                help="Check this if the first row contains column names")
    
    with col2:
        st.subheader("Processed Image")
        
        # Preprocess the image
        processed_image = preprocess_image(image, enhance_contrast, sharpen, denoise, binarize)
        st.image(processed_image, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Extracted Table")
    
    with st.spinner("Processing image..."):
        # Extract text using Tesseract OCR on processed image
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Parse the extracted text into a table
        lines = extracted_text.strip().split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        # Try to split each line into columns
        table_data = []
        for line in lines:
            # Split by multiple spaces or tabs
            row = re.split(r'\s{2,}|\t+', line)
            row = [cell.strip() for cell in row if cell.strip()]
            if row:
                table_data.append(row)
        
        if table_data:
            # Determine max columns
            max_cols = max(len(row) for row in table_data)
            
            # Pad rows to have equal columns
            for row in table_data:
                while len(row) < max_cols:
                    row.append('')
            
            # Create DataFrame based on header selection
            if has_header and len(table_data) > 1:
                df = pd.DataFrame(table_data[1:], columns=table_data[0])
            else:
                # No header - use default column names
                df = pd.DataFrame(table_data)
                df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
            
            # Try to convert numeric columns
            for col in df.columns:
                try:
                    # Remove common numeric separators and convert
                    df[col] = df[col].str.replace(',', '').str.replace('$', '').str.strip()
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
            
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Download Options")
            
            col_a, col_b = st.columns(2)
            
            # CSV download
            with col_a:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="table_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Excel download
            with col_b:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                
                st.download_button(
                    label="📥 Download as XLSX",
                    data=buffer.getvalue(),
                    file_name="table_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            st.success("✅ Table extracted successfully!")
        else:
            st.error("❌ Could not extract table data. Please ensure the image contains a clear table.")
    
    with st.expander("📝 Raw Extracted Text"):
        st.text(extracted_text)

st.markdown("---")
st.markdown("**💡 Tips for best results:**")
st.markdown("- Use the preprocessing options in the sidebar to enhance image quality")
st.markdown("- Enable 'Binarize' for tables with very clear borders and text")
st.markdown("- Try different preprocessing combinations if results aren't satisfactory")
st.markdown("- Ensure the table has clear borders and good contrast")
st.markdown("- Use high-resolution images for better accuracy")
st.markdown("- Tables with aligned columns work best")
