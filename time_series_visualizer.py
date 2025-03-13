import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1️⃣ Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# 2️⃣ Bersihkan data (hapus 2.5% atas dan bawah)
df = df[
    (df["value"] >= df["value"].quantile(0.025)) & 
    (df["value"] <= df["value"].quantile(0.975))
]

# 3️⃣ Line Plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    fig.savefig('line_plot.png')
    return fig

# 4️⃣ Bar Plot
def draw_bar_plot():
    df_bar = df.copy()
    df_bar["Year"] = df_bar.index.year
    df_bar["Month"] = df_bar.index.month
    df_bar = df_bar.groupby(["Year", "Month"])["value"].mean().unstack()

    fig = df_bar.plot(kind="bar", figsize=(12, 6), legend=True).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
    fig.savefig('bar_plot.png')
    return fig

# 5️⃣ Box Plot
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    # Pastikan tidak ada nilai NaN
    df_box = df_box.dropna()

    # Konversi kolom agar sesuai dengan Seaborn
    df_box['Year'] = df_box['date'].dt.year.astype(str)
    df_box['Month'] = df_box['date'].dt.strftime('%b')

    # Urutan bulan yang benar
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # 🔹 Perbaikan utama: Gunakan float64
    df_box["value"] = df_box["value"].astype(np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise Box Plot
    sns.boxplot(x="Year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot
    sns.boxplot(x="Month", y="value", data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig
