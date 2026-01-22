import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import io
import re
import numpy as np

st.set_page_config(page_title="Table Screenshot to Excel/CSV", page_icon="📊", layout="wide")

def preprocess_image(image, contrast=1.0, sharpness=1.0, brightness=1.0, denoise=False, binarize=False, threshold=128):
    """
    Preprocess image to improve OCR accuracy with adjustable levels
    
    Args:
        image: PIL Image object
        contrast: Contrast level (1.0 = original, >1.0 = more contrast)
        sharpness: Sharpness level (1.0 = original, >1.0 = sharper)
        brightness: Brightness level (1.0 = original, >1.0 = brighter)
        denoise: Boolean to apply noise reduction
        binarize: Boolean to convert to black & white
        threshold: Threshold for binarization (0-255)
    """
    processed = image.copy()
    
    # Convert to RGB if needed
    if processed.mode != 'L' and processed.mode != 'RGB':
        processed = processed.convert('RGB')
    
    # Denoise first (if enabled)
    if denoise:
        processed = processed.filter(ImageFilter.MedianFilter(size=3))
    
    # Adjust brightness
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(processed)
        processed = enhancer.enhance(brightness)
    
    # Enhance contrast
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(processed)
        processed = enhancer.enhance(contrast)
    
    # Enhance sharpness
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(processed)
        processed = enhancer.enhance(sharpness)
    
    # Apply additional edge enhancement for high sharpness
    if sharpness > 2.0:
        processed = processed.filter(ImageFilter.EDGE_ENHANCE)
    
    # Binarize (convert to pure black and white)
    if binarize:
        processed = processed.convert('L')
        processed = ImageOps.autocontrast(processed)
        processed = processed.point(lambda p: 255 if p > threshold else 0)
    
    return processed

def parse_table_data(extracted_text, expected_columns=None):
    """
    Parse extracted text into table data with optional column hint
    """
    lines = extracted_text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    table_data = []
    
    if expected_columns:
        # Use column count hint for better parsing
        for line in lines:
            # Try multiple splitting strategies
            # Strategy 1: Split by multiple spaces or tabs
            row = re.split(r'\s{2,}|\t+', line)
            row = [cell.strip() for cell in row if cell.strip()]
            
            # Strategy 2: If we don't have expected columns, try single space split
            if len(row) != expected_columns:
                row = line.split()
                row = [cell.strip() for cell in row if cell.strip()]
            
            # Strategy 3: Try to intelligently group tokens
            if len(row) > expected_columns:
                # Too many columns - try to merge adjacent tokens
                new_row = []
                i = 0
                while i < len(row) and len(new_row) < expected_columns:
                    if len(new_row) == expected_columns - 1:
                        # Last column - join remaining
                        new_row.append(' '.join(row[i:]))
                        break
                    else:
                        new_row.append(row[i])
                        i += 1
                row = new_row
            elif len(row) < expected_columns and len(row) > 0:
                # Too few columns - pad with empty strings
                while len(row) < expected_columns:
                    row.append('')
            
            if row and len(row) == expected_columns:
                table_data.append(row)
    else:
        # Original parsing method without column hint
        for line in lines:
            row = re.split(r'\s{2,}|\t+', line)
            row = [cell.strip() for cell in row if cell.strip()]
            if row:
                table_data.append(row)
    
    return table_data

st.title("📊 Table Screenshot Converter")
st.markdown("Upload a screenshot of a table, and I'll convert it to CSV or XLSX format")

uploaded_file = st.file_uploader("Choose an image file (JPG or PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Preprocessing options in sidebar
    st.sidebar.subheader("🔧 Image Preprocessing")
    st.sidebar.markdown("Adjust enhancement levels for better OCR results")
    
    # Contrast enhancement slider
    contrast_level = st.sidebar.slider(
        "Contrast Enhancement",
        min_value=0.0,
        max_value=3.0,
        value=2.0,
        step=0.1,
        help="1.0 = original, >1.0 = more contrast, <1.0 = less contrast"
    )
    
    # Sharpness enhancement slider
    sharpness_level = st.sidebar.slider(
        "Sharpness",
        min_value=0.0,
        max_value=3.0,
        value=1.5,
        step=0.1,
        help="1.0 = original, >1.0 = sharper edges, <1.0 = softer"
    )
    
    # Brightness adjustment slider
    brightness_level = st.sidebar.slider(
        "Brightness",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="1.0 = original, >1.0 = brighter, <1.0 = darker"
    )
    
    # Denoise checkbox (keep this as binary)
    denoise = st.sidebar.checkbox("Reduce Noise", value=True,
                                  help="Removes noise and artifacts from the image")
    
    # Binarize checkbox with threshold slider
    binarize = st.sidebar.checkbox("Binarize (Black & White)", value=False,
                                   help="Convert to pure black and white - best for clear tables")
    
    threshold = 128
    if binarize:
        threshold = st.sidebar.slider(
            "Binarization Threshold",
            min_value=0,
            max_value=255,
            value=128,
            step=5,
            help="Lower = more black, Higher = more white"
        )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Quick presets:**")
    col_preset1, col_preset2 = st.sidebar.columns(2)
    
    if col_preset1.button("Clear Table", use_container_width=True):
        st.session_state.preset = "clear"
    if col_preset2.button("Low Quality", use_container_width=True):
        st.session_state.preset = "low_quality"
    
    # Apply presets if button clicked
    if 'preset' in st.session_state:
        if st.session_state.preset == "clear":
            contrast_level = 1.5
            sharpness_level = 2.0
            brightness_level = 1.0
            denoise = False
            binarize = True
            threshold = 128
        elif st.session_state.preset == "low_quality":
            contrast_level = 2.5
            sharpness_level = 2.5
            brightness_level = 1.2
            denoise = True
            binarize = False
        del st.session_state.preset
    
    st.sidebar.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        # Ask if table has header row
        has_header = st.checkbox("Table has a header row", value=True, 
                                help="Check this if the first row contains column names")
        
        # Ask for number of columns
        use_column_hint = st.checkbox("Specify number of columns", value=False,
                                     help="Enable this if the table has a specific number of columns")
        
        expected_columns = None
        if use_column_hint:
            expected_columns = st.number_input("Number of columns", min_value=1, max_value=20, value=3,
                                              help="Enter the expected number of columns in your table")
    
    with col2:
        st.subheader("Processed Image")
        
        # Preprocess the image with slider values
        processed_image = preprocess_image(
            image, 
            contrast=contrast_level,
            sharpness=sharpness_level,
            brightness=brightness_level,
            denoise=denoise,
            binarize=binarize,
            threshold=threshold
        )
        st.image(processed_image, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Extracted Table")
    
    with st.spinner("Processing image..."):
        # Extract text using Tesseract OCR on processed image
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Parse the extracted text into a table with optional column hint
        table_data = parse_table_data(extracted_text, expected_columns)
        
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
st.markdown("- **Adjust sliders in the sidebar** for fine-tuned image enhancement")
st.markdown("- **Use Quick Presets** for common scenarios (Clear Table or Low Quality)")
st.markdown("- **Contrast slider**: Increase for faint text, decrease if text is bleeding together")
st.markdown("- **Sharpness slider**: Increase to make borders clearer")
st.markdown("- **Brightness slider**: Adjust if image is too dark or too light")
st.markdown("- **Binarize threshold**: Lower for darker tables, higher for lighter tables")
st.markdown("- **Enable 'Specify number of columns'** if you know the exact column count - this greatly improves accuracy")
st.markdown("- Use high-resolution images for better accuracy")
st.markdown("- Tables with aligned columns work best")
