import streamlit as st
from PIL import Image
import io
import os

def resize_signature(file, width=140, height=60, quality=95):
    """
    Resize signature image (returns PIL image + file size check).
    """
    img = Image.open(file).convert("RGB")
    img_resized = img.resize((width, height))

    # Save to buffer
    buffer = io.BytesIO()
    img_resized.save(buffer, format="JPEG", quality=quality, optimize=True)
    size_kb = buffer.getbuffer().nbytes // 1024

    # Adjust quality if outside 10–20 KB
    if size_kb < 10 or size_kb > 20:
        new_quality = 85 if size_kb > 20 else 100
        buffer = io.BytesIO()
        img_resized.save(buffer, format="JPEG", quality=new_quality, optimize=True)
        size_kb = buffer.getbuffer().nbytes // 1024

    buffer.seek(0)
    return img_resized, buffer, size_kb


# --- Streamlit UI ---
st.set_page_config(page_title="Signature Resizer", page_icon="✍️", layout="centered")

st.title("✍️ Signature Resizer")
st.write("Upload your signature image. It will be resized to **140x60 px** and saved as JPEG (~10–20 KB).")

# Upload file
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp", "tif"])

if uploaded_file:
    # Process image
    img_resized, buffer, size_kb = resize_signature(uploaded_file)

    # Show preview
    st.image(img_resized, caption=f"Preview ({img_resized.width}x{img_resized.height}px)", use_column_width=False)
    st.info(f"File Size: ~{size_kb} KB")

    # Download button
    st.download_button(
        label="📥 Download Resized Signature",
        data=buffer,
        file_name="signature_resized.jpg",
        mime="image/jpeg"
    )
