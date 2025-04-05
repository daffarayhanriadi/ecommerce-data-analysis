import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st


# Filter Data by Date Input
@st.cache_data
def filtered(df, start_date, end_date):
    """Menyaring data berdasarkan rentang tanggal tertentu."""
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    df = df[
        (df["order_purchase_timestamp"] >= start_date)
        & (df["order_purchase_timestamp"] <= end_date)
    ]
    return df


# Question 1
@st.cache_data
def order_revenue_trend(df, ref):
    """Menghitung jumlah pesanan per bulan dari dataset transaksi."""
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M")
    if ref == "order_id":
        df = df.groupby(by="month")[ref].count().reset_index()
        df.columns = ["month", "order"]
    else:
        df = df.groupby(by="month")[ref].sum().reset_index()
        df.columns = ["month", "revenue"]
    return df


# Question 2
@st.cache_data
def top_lowest_type_order(df):
    """Menghitung dan mencari jumlah pesanan tertinggi dan terendah berdasarkan tipe produk."""
    df = df.groupby("product_category_name")["order_item_id"].sum().reset_index()
    df.columns = ["product_type", "total_order"]
    top_df = df.sort_values("total_order", ascending=False).reset_index(drop=True)
    lowest_df = df.sort_values("total_order", ascending=True).reset_index(drop=True)
    return top_df, lowest_df


@st.cache_data
def top_lowest_type_sales(df):
    """Menghitung dan mencari jumlah pendapatan tertinggi dan terendah berdasarkan tipe produk."""
    df = df.groupby("product_category_name")["price"].sum().reset_index()
    df.columns = ["product_type", "revenue"]
    top_df = df.sort_values("revenue", ascending=False).reset_index(drop=True)
    lowest_df = df.sort_values("revenue", ascending=True).reset_index(drop=True)
    return top_df, lowest_df


# Question 3
@st.cache_data
def top_payment_methods(df):
    """Menghitung metode pembayaran terbanyak"""
    df = (
        df.groupby("payment_type")
        .agg({"order_id": "count", "payment_value": "sum"})
        .sort_values(by="order_id", ascending=False)
        .reset_index()
    )
    df.rename(columns={"order_id": "transaction_count"}, inplace=True)
    return df


# Question 4
@st.cache_data
def top_city_transaction(df):
    """Menghitung jumlah transaksi per kota."""
    df = (
        df["customer_city"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=False)
    )
    df.rename(
        columns={
            "count": "transaction_amount",
        },
        inplace=True,
    )
    return df


# Advanced Analysis
@st.cache_data
def geo_top_city_transactions(df):
    """Menghitung transaksi terbanyak berdasarkan kota"""
    city_counts = df["customer_city"].value_counts().reset_index()
    city_counts.columns = ["customer_city", "transaction_amount"]
    df = df.merge(city_counts, on="customer_city", how="left")
    return df


# Visualization Function
def order_revenue_trend_viz(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        df["month"].astype(str),
        df["order" if "order" in df else "revenue"],
        marker="o",
        linestyle="-",
        color="b",
    )
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticklabels(df["month"].astype(str), rotation=45)
    return fig


def top_lowest_order_revenue_viz(top, lowest, title):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    x = "total_order" if "total_order" in top else "revenue"
    
    sns.barplot(
        x=x,
        y="product_type",
        data=top.head(5),
        palette=colors,
        ax=ax[0],
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Total Order", fontsize=30)
    ax[0].set_title(f"Tipe Produk {title} Tertinggi", fontsize=50)
    ax[0].tick_params(axis="y", labelsize=35)
    ax[0].tick_params(axis="x", labelsize=30)

    sns.barplot(
        x=x,
        y="product_type",
        data=lowest.sort_values(by=x, ascending=True).head(5),
        palette=colors,
        ax=ax[1],
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Total Order", fontsize=30)
    ax[1].set_title(f"Tipe Produk {title} Terendah", fontsize=50)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].tick_params(axis="y", labelsize=35)
    ax[1].tick_params(axis="x", labelsize=30)
    return fig


def payment_type_distributions_viz(df, ref):
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y=ref,
        x="payment_type",
        data=df,
        palette=colors_,
    )
    ax.set_title(
        "Jumlah Transaksi Dari Masing-Masing Metode Pembayaran",
        loc="center",
        fontsize=15,
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="x", labelsize=12)
    return fig


# Set tema & title dashboard
sns.set(style="dark")
st.header(":shopping_trolley: E-Commerce Dashboard :shopping_trolley:")

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/main_data.csv"
    )

# Menangani Tipe Data
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# Sidebar
with st.sidebar:

    # Github
    st.markdown(
        "<h3 style='text-align: center;'> 🔗 GitHub Repository</h3>",
        unsafe_allow_html=True,
    )
    github_logo_url = "https://cdn-icons-png.flaticon.com/512/25/25231.png"
    repo_url = "https://github.com/daffarayhanriadi/ecommerce-data-analysis"
    st.markdown(
                f"""
                    <div style="display: flex; justify-content: center;">
                        <a href="{repo_url}" target="_blank">
                            <img src="{github_logo_url}" width="70">
                        </a>
                    </div>
                """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Filter Tanggal
    st.subheader(":chart_with_upwards_trend: Filter Data")
    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()
    start_date = st.date_input(
        label="Start Date",
        min_value=min_date,
        value=min_date,
    )
    end_date = st.date_input(
        label="End Date",
        max_value=pd.Timestamp("2018-08-29"),
        value=max_date,
    )
    filtered_df = filtered(df, start_date, end_date)
    st.markdown("---")

    # Sumber Data
    st.subheader(":bar_chart: Data Source")
    st.markdown(
                """
                    :link: [**Brazilian E-Commerce Dataset**](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
                    *Explore real-world e-commerce transactions in Brazil!*
                """
    )
    st.markdown("---")

    # Owner
    st.markdown(
                """
                    :pushpin: **Created by:** Daffa Rayhan Riadi  
                    :e-mail: **Contact:** [Email](mailto:daffarayhanriadi@gmail.com)  
                """
    )

# 1. Tren Penjualan per Bulan
# - Tren Jumlah Pesanan per Bulan
st.write("")
st.write("")
st.write("")
st.subheader("Tren Penjualan per Bulan (Berdasarkan Jumlah Pesanan)")
order_trend = order_revenue_trend(filtered_df, "order_id")
order_trend_fig = order_revenue_trend_viz(order_trend)
st.pyplot(order_trend_fig)
st.markdown("###### Tabel Lengkap Tren Penjualan per Bulan (Berdasarkan Jumlah Pesanan)")
st.write(order_trend)

# - Tren Jumlah Pendapatan per Bulan
st.write("")
st.write("")
st.write("")
st.subheader("Tren Tren Penjualan per Bulan (Berdasarkan Jumlah Pendapatan)")
revenue_trend = order_revenue_trend(filtered_df, "price")
revenue_trend_fig = order_revenue_trend_viz(revenue_trend)
st.pyplot(revenue_trend_fig)
st.markdown("###### Tabel Lengkap Tren Tren Penjualan per Bulan (Berdasarkan Jumlah Pendapatan)")
st.write(revenue_trend)
with st.expander("Bagaimana tren penjualan dalam beberapa bulan terakhir?"):
    st.write(
            """
                Berdasarkan visualisasi diatas dapat terlihat adanya **tren kenaikan** penjualan dari tahun 2016 hingga akhir 2018. Kenaikan ini cukup signifikan pada pertengahan 2017, menunjukkan pertumbuhan bisnis e-commerce yang positif, baik dari sisi volume transaksi maupun revenue. 

                Terdapat lonjakan besar pada November 2017, kemungkinan karena terdapat sebuah event sehingga dapat meningkatkan pesanan maupun pendapatan. Setelah itu, penjualan tetap tinggi meskipun mengalami sedikit fluktuasi pada 2018. Ini bisa menandakan bahwa pasar sudah mencapai titik keseimbangan setelah fase pertumbuhan yang cepat.

                Dapat dilihat pula bahwa pola pada kedua grafik mirip, yang menunjukkan bahwa pertumbuhan jumlah pesanan berkontribusi langsung terhadap kenaikan pendapatan.
            """
    )

# 2. Produk dengan Penjualan Tertinggi dan Terendah
# - Produk dengan Pesanan Tertinggi dan Terendah
st.write("")
st.write("")
st.write("")
st.subheader("Distribusi Penjualan Produk Pada E-Commerce (Berdasarkan Pesanan)")
top_type_order, lowest_type_order = top_lowest_type_order(filtered_df)
top_lowest_order_fig = top_lowest_order_revenue_viz(top_type_order, lowest_type_order, "Pesanan")
st.pyplot(top_lowest_order_fig)
st.markdown("###### Distribusi Penjualan Produk Pada E-Commerce (Berdasarkan Pesanan)")
st.write(top_type_order)


# - Produk dengan Pendapatan Tertinggi dan Terendah
st.write("")
st.write("")
st.write("")
st.subheader("Distribusi Penjualan Produk Pada E-Commerce (Berdasarkan Pendapatan)")
top_type_revenue, lowest_type_revenue = top_lowest_type_sales(filtered_df)
top_lowest_revenue_fig = top_lowest_order_revenue_viz(top_type_revenue, lowest_type_revenue, "Pendapatan")
st.pyplot(top_lowest_revenue_fig)
st.markdown("###### Distribusi Penjualan Produk Pada E-Commerce (Berdasarkan Pendapatan)")
st.write(top_type_revenue)
with st.expander("Bagaimana distribusi penjualan produk pada e-commerce?"):
    st.write(
            """
                Berdasarkan visualisasi diatas bahwa dalam hal pesanan, tipe produk **bed_bath_table** memiliki jumlah pesanan tertinggi, dengan kata lain tipe produk ini yang paling populer dalam hal volume penjualan, diikuti furniture_decor, health_beauty, sports_leisure, dan computers_accessories. Tipe produk ini cenderung berkaitan dengan kebutuhan rumah tangga, kecantikan, dan gaya hidup, yang menunjukkan bahwa pelanggan lebih sering membeli produk yang berkaitan dengan kebutuhan sehari-hari.

                Sebaliknya, tipe produk **security_and_services** memiliki jumlah pesanan terendah, jauh di bawah tipe produk lainnya, diikuti fashion_childrens_clothes, pc_gamer, cds_dvds_musicals, dan la_cuisine. Ini menunjukkan bahwa produk seperti jasa keamanan, pakaian anak-anak, perlengkapan gaming, media fisik (CD/DVD), dan peralatan dapur khusus kurang diminati atau memiliki pasar yang lebih kecil.

                Kemudian dalam hal pendapatan, tipe produk **health_beauty** memimpin dalam menghasilkan revenue (meskipun bukan yang paling banyak dipesan), diikuti oleh watches_gifts, bed_bath_table, sports_leisure, dan computers_accessories. Ini menunjukkan bahwa meskipun volume penjualannya tidak selalu tinggi, harga produk atau nilai transaksi per pesanan dalam tipe produk ini cukup besar.

                Sebaliknya, tipe produk **security_and_services** memiliki jumlah pendapatan yang paling rendah, diikuti fashion_childrens_clothes, cds_dvds_musicals, home_comfort_2, dan flowers.  Hal ini menunjukkan bahwa tipe produk tersebut tidak hanya jarang dibeli, tetapi juga memiliki nilai jual yang relatif rendah.
             """
    )


# 3. Distribusi Metode Pembayaran Terpopuler
# - Distribusi Berdasarkan Jumlah Transaksi
st.write("")
st.write("")
st.write("")
st.subheader("Distribusi Metode Pembayaran Terpopuler (Berdasarkan Transaksi)")
payment_type_distributions = top_payment_methods(filtered_df)
top_payment_methods_fig = payment_type_distributions_viz(payment_type_distributions, "transaction_count")
st.pyplot(top_payment_methods_fig)
st.markdown("###### Tabel Lengkap Distribusi Metode Pembayaran Terpopuler (Berdasarkan Transaksi)")
st.write(payment_type_distributions.loc[:, ["payment_type", "transaction_count"]])

# - Distribusi Berdasarkan Total Nilai Pembayaran
st.write("")
st.write("")
st.write("")
st.subheader("Distribusi Metode Pembayaran Terpopuler (Berdasarkan Total Nilai Pembayaran)")
top_payment_methods_fig = payment_type_distributions_viz(payment_type_distributions, "payment_value")
st.pyplot(top_payment_methods_fig)
st.markdown("###### Tabel Lengkap Distribusi Metode Pembayaran Terpopuler (Berdasarkan Total Nilai Pembayaran)")
st.write(payment_type_distributions.loc[:, ["payment_type", "payment_value"]])
with st.expander("Bagaimana distribusi pengguna metode pembayaran yang sering di lakukan oleh pelanggan?"):
    st.write(
            """
                Berdasarkan visualisasi diatas didapatkan bahwa metode pembayaran yang paling sering digunakan adalah **creadit_card** dengan jumlah transaksi dan total nilai pembayaran yang jauh lebih tinggi dibandingkan metode lainnya. Hal ini menunjukkan bahwa pelanggan lebih cenderung menggunakan kartu kredit, kemungkinan karena kemudahan, fleksibilitas, atau promo cicilan yang tersedia pada e-commerce.

                Boleto, yang merupakan metode pembayaran berbasis slip pembayaran di Brazil, menempati posisi kedua dengan jumlah transaksi dan total nilai pembayaran yang cukup signifikan, meskipun masih jauh di bawah kartu kredit. Ini menunjukkan bahwa ada segmen pelanggan yang lebih nyaman menggunakan metode pembayaran non-kartu, atau bisa saja pelanggan yang belum memiliki akses ke kartu kredit.

                Voucher dan debit card memiliki jumlah transaksi yang sangat rendah, menunjukkan bahwa metode ini kurang diminati oleh pelanggan dan penggunaannya masih terbatas.
             """
    )

# 4. Kota dengan Transaksi Terbanyak
st.write("")
st.write("")
st.write("")
st.subheader("Top 5 Kota Berdasarkan Jumlah Transaksi")
top_city_transactions = top_city_transaction(filtered_df)
top_city_transactions_viz = top_city_transactions.head(5)
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#72BCD4" if i == 0 else "#D3D3D3" for i in range(len(top_city_transactions_viz))]
ax.barh(
    top_city_transactions_viz["customer_city"],
    top_city_transactions_viz["transaction_amount"],
    color=colors,
)
ax.set_title("Top 5 Kota Berdasarkan Jumlah Transaksi")
ax.invert_yaxis()
st.pyplot(fig)
st.markdown("###### Tabel Lengkap Kota Dengan Jumlah Transaksi Terbanyak")
st.write(top_city_transactions)
with st.expander("Kota mana yang memiliki jumlah transaksi terbanyak berdasarkan data pelanggan?"):
    st.write(
            """
                Berdasarkan visualisasi diatas diketahui bahwa **Sao Paulo** memiliki jumlah transaksi yang jauh lebih tinggi dibandingkan kota lainnya, menunjukkan bahwa kota ini adalah pasar utama untuk bisnis e-commerce. Hal ini bisa disebabkan oleh populasi yang besar, daya beli yang tinggi, atau infrastruktur e-commerce yang lebih baik maupun kota yang lebih maju.

                Rio de Janeiro berada di posisi kedua, meskipun jumlah transaksinya jauh lebih rendah dibandingkan Sao Paulo. Ini menunjukkan bahwa meskipun Rio de Janeiro memiliki pasar besar, potensinya mungkin belum dimanfaatkan secara maksimal dibandingkan Sao Paulo.

                Sedangkan Belo Horizonte, Brasilia, dan Curitiba, ketiga kota ini menunjukkan jumlah transaksi yang signifikan tetapi masih jauh lebih rendah dibandingkan dua kota teratas.
             """
    )

st.subheader("Kesimpulan - 1")
st.write(
        """
            - Berdasarkan hasil analisis, bisnis e-commerce menunjukkan pertumbuhan positif dari tahun 2016 hingga 2018, dengan lonjakan signifikan pada November 2017 yang kemungkinan dipengaruhi oleh event atau promosi besar. Tren penjualan yang meningkat sejalan dengan pertumbuhan pendapatan, menandakan korelasi positif antara volume transaksi dan revenue.  

            - Dalam analisis produk, kategori **bed_bath_table** memiliki jumlah pesanan tertinggi, sementara **health_beauty** menghasilkan pendapatan tertinggi. Di sisi lain, **security_and_services** merupakan kategori dengan pesanan dan pendapatan terendah, yang menunjukkan potensi pasar yang lebih kecil untuk kategori ini.  

            - Metode pembayaran yang paling banyak digunakan adalah **kartu kredit**, menunjukkan bahwa pelanggan lebih memilih kemudahan pembayaran digital dibandingkan metode lain seperti boleto atau debit card.  

            - Dari segi wilayah, **Sao Paulo** mendominasi jumlah transaksi, menjadikannya pasar utama e-commerce, sementara kota-kota lain seperti **Rio de Janeiro, Belo Horizonte, Brasilia,** dan **Curitiba** masih memiliki potensi pertumbuhan yang bisa dioptimalkan lebih lanjut.  
        """
)

# Analisis Lanjutan
st.write("")
st.write("")
st.write("")
st.subheader("Analisis Lanjutan")
fig = px.scatter_mapbox(
    filtered_df,
    lat="geolocation_lat",
    lon="geolocation_lng",
    hover_name="customer_city",
    title="Geoanalysis Distribusi Pelanggan di Brazil",
    zoom=4,
    height=600,
    color_discrete_sequence=["blue"],
    mapbox_style="open-street-map",
)
fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig)
with st.expander("Insight - Geoanalysis Distribusi Pelanggan di Brazil"):
    st.text(
            """
                Tampilan diatas adalah tampilan dari Scatter Mapbox dari distribusi transaksi yang terdapat di Brazil berdasarkan pelanggan.
                
                Sebagian besar pelanggan terkonsentrasi di wilayah tenggara dan timur Brazil, terutama di sekitar kota besar seperti São Paulo, Rio de Janeiro, dan Belo Horizonte.
                
                Banyaknya pelanggan di wilayah tersebut dapat didasari oleh pusat ekonomi dan bisnis maupun kemajuan dari kota tersebut.
            """
    )

st.write("")
st.write("")
st.write("")
geo_top_city_transactions_df = geo_top_city_transactions(filtered_df)
fig_map = px.scatter_mapbox(
    geo_top_city_transactions_df,
    lat="geolocation_lat",
    lon="geolocation_lng",
    size="transaction_amount",
    hover_name="customer_city",
    title="Geoanalysis Kota dengan Pelanggan Terbanyak",
    hover_data={
        "geolocation_lat": False,
        "geolocation_lng": False,
        "transaction_amount": True,
    },
    zoom=4,
    color="transaction_amount",
    color_continuous_scale="Blues",
    mapbox_style="carto-positron",
)
fig_map.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=50, b=0))
st.plotly_chart(fig_map)
with st.expander("Insight - Geoanalysis Kota dengan Pelanggan Terbanyak"):
    st.text(
            """
                Dapat dilihat berdasarkan Scatter Mapbox diatas bahwa warna (semakin gelap) dan ukuran titik (semakin besar) menunjukkan jumlah transaksi dengan Kota São Paulo memiliki transaksi terbesar dibandingkan kota lainnya.
            
                Meskipun tidak sebesar Kota São Paulo, dapat dilihat pula bahwa Kota Rio de Janeiro juga menunjukkan jumlah transaksi yang cukup tinggi.
            """
    )

st.subheader("Kesimpulan - 2")
st.write(
        """
            - Sebaran transaksi e-commerce di Brazil paling banyak terkonsentrasi di wilayah tenggara dan timur, terutama di kota-kota besar seperti São Paulo, Rio de Janeiro, dan Belo Horizonte. Hal ini kemungkinan dipengaruhi oleh faktor ekonomi, bisnis, dan perkembangan infrastruktur di daerah tersebut.

            - Kota São Paulo memiliki jumlah transaksi tertinggi dibandingkan kota lain, dengan ukuran dan warna titik yang lebih mencolok. Sementara itu, Kota Rio de Janeiro juga menunjukkan aktivitas transaksi yang cukup tinggi, meskipun tidak sebesar São Paulo.
        """
)

st.write("")
st.write("")
st.write("")
st.subheader("Rekomendasi")
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Pengoptimalan Produk Populer",
        "Strategi Peningkatan Revenue",
        "Diversifikasi Metode Pembayaran",
        "Ekspanasi Pasar",
    ]
)
with tab1:
    st.write(
        """
                - Meningkatkan stok dan variasi produk dalam kategori **bed_bath_table, health_beauty**, dan **computers_accessories** untuk memenuhi permintaan pasar.
                - Menawarkan promosi atau diskon pada produk kategori dengan penjualan rendah untuk meningkatkan minat pelanggan.
        """
    )
with tab2:
    st.write(
        """
                - Mendorong penjualan produk dengan nilai transaksi tinggi seperti **health_beauty** dengan kampanye pemasaran yang lebih agresif.
                - Menggabungkan strategi cross-selling dan up-selling untuk meningkatkan nilai rata-rata transaksi per pelanggan.
        """
    )
with tab3:
    st.write(
        """
                - Meningkatkan edukasi pelanggan tentang opsi pembayaran lain seperti debit card dan voucher untuk menjangkau lebih banyak segmen pelanggan.  
                - Menyediakan insentif seperti cashback atau diskon untuk metode pembayaran alternatif guna mendorong penggunaannya.     
        """
    )
with tab4:
    st.write(
        """
                - Mengembangkan strategi pemasaran dan logistik untuk meningkatkan transaksi di kota-kota potensial seperti **Rio de Janeiro, Belo Horizonte, Brasilia**, dan **Curitiba**.  
                - Mengidentifikasi hambatan dalam adopsi e-commerce di kota-kota dengan transaksi lebih rendah untuk meningkatkan penetrasi pasar.  
        """
    )

st.markdown("---")
st.caption(
    "Copyright © 2025 | Daffa Rayhan Riadi - Laskar AI Cohort | Passionate in Data Analytics & Artificial Intelligence"
)
