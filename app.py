import streamlit as st
import csv
import os.path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# CSV dosyasını kontrol et ve varsa yükle
data_file = "kisiler.csv"
if os.path.exists(data_file):
    with open(data_file, mode="r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
else:
    data = []


def save_to_csv(data):
    with open(data_file, mode="w", newline="") as file:
        fieldnames = ["Cinsiyet", "Boy (cm)", "Kilo (kg)"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)


def train_model():
    global data
    df = pd.DataFrame(data)
    # Cinsiyeti 0 ve 1 olarak dönüştür
    df["Cinsiyet"] = df["Cinsiyet"].apply(lambda x: 0 if x == "Erkek" else 1)
    X = df[["Boy (cm)", "Kilo (kg)"]] #emre
    y = df["Cinsiyet"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Modelin başarısını değerlendir
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Başarıyı görselleştir
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x=["Boy (cm)"], y=["Cinsiyet"], palette="Blues")
    plt.title("Cinsiyet ve Boy İlişkisi")
    st.pyplot(plt)

    return model


def main():
    st.title("Kişi Bilgi Girişi, Model Eğitimi ve Değerlendirme")

    # Kişinin bilgilerini girme
    cinsiyet = st.radio("Cinsiyet seçiniz", ("Erkek", "Kadın"))
    boy = st.number_input("Boy (cm)", min_value=0, value=0)
    kilo = st.number_input("Kilo (kg)", min_value=0, value=0)

    # Bilgileri kaydetme düğmesi
    if st.button("Bilgileri Kaydet"):
        global data
        new_row = {"Cinsiyet": cinsiyet, "Boy (cm)": boy, "Kilo (kg)": kilo}
        data.append(new_row)
        save_to_csv(data)
        st.success("Bilgiler başarıyla kaydedildi.")

    # Modeli eğitme düğmesi
    if st.button("Modeli Eğit ve Değerlendir"):
        model = train_model()
        st.success("Model eğitildi ve değerlendirildi.")

    # Veriyi görüntüleme düğmesi
    if st.button("Veriyi Görüntüle"):
        df = pd.DataFrame(data)
        st.dataframe(df)


if __name__ == "__main__":
    main()
