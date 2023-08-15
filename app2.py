import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_FILE = "veriler.csv"

def save_data_to_csv(data):
    df = pd.DataFrame(data)
    if not os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        existing_data = pd.read_csv(DATA_FILE)
        combined_data = pd.concat([existing_data, df], ignore_index=True)
        combined_data.to_csv(DATA_FILE, index=False)

def main():
    st.title("Veri Girişi, Kaydetme ve Görselleştirme Uygulaması")

    data = []

    st.subheader("Veri Girişi")
    cinsiyet = st.selectbox("Cinsiyet seçiniz", ("Erkek", "Kadın"))
    boy = st.number_input("Boy (cm)", min_value=0)
    kilo = st.number_input("Kilo (kg)", min_value=0)

    # Veriyi kaydetmek için düğme
    if st.button("Kaydet"):
        data.append({"Cinsiyet": cinsiyet, "Boy (cm)": boy, "Kilo (kg)": kilo})
        save_data_to_csv(data)
        st.success("Veri başarıyla kaydedildi.")

    # CSV verilerini oku
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)

        # Görselleştirme
        st.subheader("Boy ve Kilo Dağılımı")
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x="Boy (cm)", kde=True, bins=20)
        plt.title("Boy Dağılımı")
        st.pyplot(plt)

        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x="Kilo (kg)", kde=True, bins=20)
        plt.title("Kilo Dağılımı")
        st.pyplot(plt)

        # İşlenen veriyi görüntüleme
        st.subheader("İşlenen Veri")
        st.dataframe(df)
        # Veriyi satır bazında gösterme
        for index, row in df.iterrows():
            st.write(
                f"Satır {index + 1}: Cinsiyet: {row['Cinsiyet']}, Boy: {row['Boy (cm)']}, Kilo: {row['Kilo (kg)']}")
            if st.button(f"Satırı Sil ({index + 1})"):
                df = df.drop(index)
                df.reset_index(drop=True, inplace=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Satır başarıyla silindi.")


if __name__ == "__main__":
    main()
