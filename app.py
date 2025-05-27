import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dominant Color Picker", page_icon="🎨", layout="wide")

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #6C63FF;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #999999;
    }
    </style>
    <p class="title">🎨 Dominant Color Picker</p>
    <p class="subtitle">Unggah gambar Anda untuk mendapatkan 5 warna dominan</p>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Unggah gambar di sini (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang Diunggah", use_column_width=True)

    # Proses gambar
    with st.spinner("Mengambil warna dominan..."):
        image = image.convert('RGB')
        img_array = np.array(image)
        img_array = img_array.reshape((-1, 3))

        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(img_array)
        colors = kmeans.cluster_centers_.astype(int)

        # Tampilkan hasil
        st.subheader("Palet Warna Dominan:")

        cols = st.columns(5)
        hex_colors = []

        for idx, col in enumerate(cols):
            rgb = colors[idx]
            hex_color = '#%02x%02x%02x' % tuple(rgb)
            hex_colors.append(hex_color)
            col.color_picker(f"Warna {idx+1}", hex_color)

        # Tampilkan bar warna
        st.subheader("Palet Warna dalam Bar:")
        fig, ax = plt.subplots(figsize=(10, 2))
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=np.array(color)/255))
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 1)
        ax.axis('off')
        st.pyplot(fig)

    st.success("Warna dominan berhasil dihasilkan! 🎉")

else:
    st.info("Silakan unggah gambar terlebih dahulu.")