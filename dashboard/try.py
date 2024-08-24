import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Pertanyaan
# Pada bulan apa bike riding mendapat order terbanyak dalam periode 1 tahun?
# Pada musim apa bike riding mendapat order terbanyak dalam 1 tahun?
# Bagaimana korelasi antara suhu terhadap total order bike riding?

day = pd.read_csv('day.csv')

for col in day:
    print(col)
    print(day[col].unique())
    print('\n\n')

## Mengubah tipe data pada beberapa kolom
day['dteday'] = pd.to_datetime(day['dteday'])
day['season'] = day.season.astype('category')
day['mnth'] = day.mnth.astype('category')
day['holiday'] = day.holiday.astype('category')
day['weekday'] = day.weekday.astype('category')
day['workingday'] = day.workingday.astype('category')
day['weathersit'] = day.weathersit.astype('category')


# Mengonversi data pada kolom kategori variabel berdasarkan kriteria 
# yang ditunjukkan pada file readme.txt
day['season'] = day['season'].replace((1,2,3,4), ('springer', 'summer', 'fall', 'winter'))
day['yr'] = day['yr'].replace((0,1), (2011, 2012))
day['mnth'] = day['mnth'].replace((1,2,3,4,5,6,7,8,9,10,11,12), ('jan','feb','march','apr','may','june','july','august','sept','okt','nov','dec'))
day['holiday'] = day['holiday'].replace((0,1),('No', 'Yes'))
day['weekday'] = day['weekday'].replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
day['workingday'] = day['workingday'].replace((0,1),('No', 'Yes'))
day['weathersit'] = day['weathersit'].replace((1,2,3,4),('Clear','Misty','Light_RainSnow','Heavy_RainSnow'))

# Drop kolom yang tidak digunakan dalam data
day = day.drop(columns='instant')

# Merubah nama kolom
day = day.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "weathersit" : "weather",
    "hum" : "humidity",
    "cnt" : "total_count"}
)


# Merubah nilai dari 'temp', 'atemp', 'humidity, 'windspeed' ke dalam nilai yang belum dinormalisasi
day['temp'] = day['temp']*41
day['atemp'] = day['atemp']*50
day['humidity'] = day['humidity']*100
day['windspeed'] = day['windspeed']*67

for col in day:
    print(col)
    print(day[col].unique())
    print('\n\n')
print(day.head())
print(day.info())


### RFM ANALISIS
rfm_df = day.groupby(by="casual", as_index=False).agg({
    "date": "max", # mengambil tanggal order terakhir
    "total_count": ["nunique", "sum"], # menghitung jumlah order & menghitung jumlah revenue yang dihasilkan
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
# menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = day["date"].dt.date.max()
print(recent_date)

rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
print(rfm_df)


print('='*90)
rfm_df = day.groupby(by="registered", as_index=False).agg({
    "date": "max", # mengambil tanggal order terakhir
    "total_count": ["nunique", "sum"], # menghitung jumlah order & menghitung jumlah revenue yang dihasilkan
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
# menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = day["date"].dt.date.max()
print(recent_date)

rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
print(rfm_df)


### EDA
columns = ['casual', 'registered', 'total_count']
fig, ax = plt.subplots(1, 3, figsize=(10,5))

for i, ax in enumerate(ax):
    sns.histplot(x=day[columns[i]], ax=ax, bins=10, color='red')
    ax.set_title(columns[i])
    ax.set_xlabel("")
    ax.set_ylabel("")
plt.tight_layout()
plt.show()

# day[columns].hist(bins=15, figsize=(15, 10))
# plt.tight_layout()
# plt.show()

fig, ax = plt.subplots(1, 3, figsize=(10,5))
for i, ax in enumerate(ax):
    sns.boxplot(y=day[columns[i]], ax=ax, color='red')
    ax.set_title(columns[i])
    ax.set_xlabel("")
    ax.set_ylabel("")
plt.tight_layout()
plt.show()

# Histogram untuk casual menunjukkan right-skewed distribution.
# Histogram untuk registered dan total_count menunjukkan distribusi normal.
# Boxplot casual juga menunjukkan adanya outlier.


### HASIL ANALISIS
# Pada bulan apa bike riding mendapat order terbanyak dalam periode 1 tahun (2011)?
bulan2021 = day[day['year'] == 2011].groupby('month')['total_count'].sum().reset_index(name='jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
print(bulan2021)

# Pada bulan apa bike riding mendapat order terbanyak dalam periode 1 tahun (2012)?
bulan2022 = day[day['year'] == 2012].groupby('month')['total_count'].sum().reset_index(name='jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
print(bulan2022)

plt.figure(figsize=(10,6))
sns.barplot(x='year', y='total_count', data=day, hue='year')
plt.xlabel("Year")
plt.ylabel("Total Rides")
plt.title("Total of bikeshare rides per Years")
plt.show()


# Pada musim apa bike riding mendapat order terbanyak dalam 1 tahun (2011)?
musim2021 = day[day['year'] == 2011].groupby('season')['total_count'].sum().reset_index(name= 'jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
print(musim2021)

# Pada musim apa bike riding mendapat order terbanyak dalam 1 tahun (2012)?
musim2022 = day[day['year'] == 2012].groupby('season')['total_count'].sum().reset_index(name= 'jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
print(musim2022)

plt.figure(figsize=(10,6))
sns.barplot(x='season', y='total_count', data=day, hue='year')
plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Total of bikeshare rides per Seasons")
plt.show()

# Bagaimana korelasi antara suhu terhadap total order bike riding?
plt.figure(figsize=(10,6))
sns.scatterplot(x='temp', y='total_count', data=day, hue='season')
plt.xlabel("Temperature (degC)")
plt.ylabel("Total Rides")
plt.title("Clusters of bikeshare rides by season and temperature (2011-2012)")
# Show the plot
plt.tight_layout()
plt.show()




st.title('Dashboard Bike Sharing')

season = day['season'].unique()
month = day['month'].unique()
temp_max = day['temp'].max()
temp_min = day['temp'].min()

print(season)
print(month)
    
with st.sidebar:
    st.text('Filter')
    
    season_filter = st.multiselect(label='Season', options=season, default=season.tolist())
    month_filter = st.multiselect(label='Month', options=month, default=month.tolist())
    min, max = st.slider(label='Temperature', min_value=temp_min, max_value=temp_max, value=(temp_min, temp_max))
    
day = day[(day['season'].isin(season_filter)) & (day['month'].isin(month_filter)) & (day['temp'] >= min) & (day['temp'] <= max)]


col1, col2 = st.columns(2)
with col1:
    # Pada bulan apa bike riding mendapat order terbanyak dalam periode 1 tahun (2011)?
    bulan2021 = day[day['year'] == 2011].groupby('month')['total_count'].sum().reset_index(name='jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
    st.dataframe(data=bulan2021.head(), width=300, height=200)

with col2:
    # Pada bulan apa bike riding mendapat order terbanyak dalam periode 1 tahun (2012)?
    bulan2022 = day[day['year'] == 2012].groupby('month')['total_count'].sum().reset_index(name='jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
    st.dataframe(data=bulan2022.head(), width=300, height=200)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='year', y='total_count', data=day, hue='year')
plt.xlabel("Year")
plt.ylabel("Total Rides")
plt.title("Total of bikeshare rides per Years")
st.pyplot(fig)


col1, col2 = st.columns(2)
with col1:
    # Pada musim apa bike riding mendapat order terbanyak dalam 1 tahun (2011)?
    musim2021 = day[day['year'] == 2011].groupby('season')['total_count'].sum().reset_index(name= 'jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
    st.dataframe(data=musim2021.head(), width=300, height=200)
    
with col2:
    # Pada musim apa bike riding mendapat order terbanyak dalam 1 tahun (2012)?
    musim2022 = day[day['year'] == 2012].groupby('season')['total_count'].sum().reset_index(name= 'jumlah').sort_values('jumlah', ascending=False).reset_index(drop=True)
    st.dataframe(data=musim2022.head(), width=300, height=200)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='season', y='total_count', data=day, hue='year')
plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Total of bikeshare rides per Seasons")
st.pyplot(fig)


# Bagaimana korelasi antara suhu terhadap total order bike riding?
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='temp', y='total_count', data=day, hue='season')
plt.xlabel("Temperature (degC)")
plt.ylabel("Total Rides")
plt.title("Clusters of bikeshare rides by season and temperature (2011-2012)")
# Show the plot
plt.tight_layout()
st.pyplot(fig)
