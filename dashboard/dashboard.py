import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

sns.set(style="dark")
st.header(":shopping_trolley: E-Commerce Dashboard :shopping_trolley:")

orders_trend_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/orders_trend.csv")
selling_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/selling.csv")
top_payment_methods_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/top_payment_methods.csv")
top_city_transaction_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/top_city_transaction.csv")
geo_customer_distribution_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/geo_customer_distribution.csv")
geo_top_city_transaction_df = pd.read_csv("https://raw.githubusercontent.com/daffarayhanriadi/ecommerce-data-analysis/refs/heads/main/dashboard/geo_top_city_transaction.csv")

# 1. Tren Jumlah Pesanan per Bulan
st.write("")
st.write("")
st.write("")
st.subheader("Tren Jumlah Pesanan per Bulan (2016-2018)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    orders_trend_df["order_month"].astype(str),
    orders_trend_df["order_quantity"],
    marker="o",
    linestyle="-",
    color="b",
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticklabels(orders_trend_df["order_month"].astype(str), rotation=45)
st.pyplot(fig)
with st.expander("Bagaimana tren penjualan dalam beberapa bulan terakhir?"):
    st.write("""
                Berdasarkan visualisasi diatas dapat terlihat adanya **tren kenaikan** jumlah pesanan dari tahun 2016 hingga akhir 2017. Kenaikan ini cukup signifikan pada pertengahan 2017, menunjukkan pertumbuhan bisnis e-commerce yang stabil. 

                Terdapat lonjakan besar pada November 2017, setelah itu, jumlah pesanan tetap tinggi meskipun mengalami sedikit fluktuasi. Setelah lonjakan di akhir 2017, jumlah pesanan cenderung stabil pada 2018, meskipun ada sedikit penurunan pada pertengahan 2018. Ini bisa menandakan bahwa pasar sudah mencapai titik keseimbangan setelah fase pertumbuhan yang cepat.
            """)
st.subheader("Tabel Lengkap Jumlah Pesanan per Bulan (2016-2018)")
st.write(orders_trend_df)


# 2. Produk dengan Penjualan Tertinggi dan Terendah
st.write("")
st.write("")
st.write("")
st.subheader("Tipe Produk Penjualan Tertinggi dan Terendah")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="order_total",
    y="product_type",
    data=selling_df.head(5),
    palette=colors,
    ax=ax[0],
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Order", fontsize=30)
ax[0].set_title("Tipe Produk Penjualan Tertinggi", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

sns.barplot(
    x="order_total",
    y="product_type",
    data=selling_df.sort_values(by="order_total", ascending=True).head(5),
    palette=colors,
    ax=ax[1],
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Order", fontsize=30)
ax[1].set_title("Tipe Produk Penjualan Terendah", fontsize=50)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)
st.pyplot(fig)
with st.expander("Apa tipe produk yang memiliki penjualan tertinggi dan terendah?"):
    st.write("""
                Berdasarkan visualisasi diatas bahwa tipe produk **bed_bath_table** memiliki jumlah penjualan tertinggi dibandingkan tipe produk lainnya. Tipe produkfurniture_decor, health_beauty, sports_leisure, dan computers_accessories juga memiliki angka penjualan yang cukup tinggi. Produk-produk dalam tipe produk ini cenderung berkaitan dengan kebutuhan rumah tangga, kecantikan, dan gaya hidup, yang menunjukkan bahwa pelanggan lebih sering membeli produk yang berkaitan dengan kebutuhan sehari-hari.

                Sebaliknya tipe produk **security_and_services** memiliki jumlah penjualan terendah, jauh di bawah tipe produk lainnya. Produk dalam tipe produk fashion_childrens_clothes, pc_gamer, cds_dvds_musicals, dan la_cuisine juga memiliki angka penjualan yang sangat rendah. Ini menunjukkan bahwa produk seperti jasa keamanan, pakaian anak-anak, perlengkapan gaming, media fisik (CD/DVD), dan peralatan dapur khusus kurang diminati atau memiliki pasar yang lebih kecil.
             """)
st.subheader("Tabel Lengkap Penjualan Per Tipe Produk")
st.write(selling_df)

# 3. Metode Pembayaran Terpopuler
st.write("")
st.write("")
st.write("")
st.subheader("Metode Pembayaran yang Paling Sering Digunakan")
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="transaction_amount",
    x="payment_type",
    data=top_payment_methods_df.sort_values(by="transaction_amount", ascending=False),
    palette=colors_,
    ax=ax,
)
st.pyplot(fig)
with st.expander("Apa metode pembayaran yang paling sering digunakan oleh pelanggan?"):
    st.write("""
                Berdasarkan visualisasi diatas didapatkan bahwa metode pembayaran yang paling sering digunakan adalah **kartu kredit** dengan jumlah transaksi yang jauh lebih tinggi dibandingkan metode lainnya. Hal ini menunjukkan bahwa pelanggan lebih cenderung menggunakan kartu kredit.

                Boleto, yang merupakan metode pembayaran berbasis slip pembayaran di Brazil, menempati posisi kedua dengan jumlah transaksi yang cukup signifikan, meskipun masih jauh di bawah kartu kredit. Ini menunjukkan bahwa ada segmen pelanggan yang lebih nyaman menggunakan metode pembayaran non-kartu.

                Voucher dan debit card memiliki jumlah transaksi yang sangat sedikit, menunjukkan bahwa metode ini kurang diminati oleh pelanggan. Kategori not_defined sangat kecil, yang berarti sebagian besar transaksi memiliki metode pembayaran yang jelas.
             """)
st.subheader("Tabel Lengkap Metode Pembayaran Yang Paling Sering Digunakan")
st.write(top_payment_methods_df)

# 4. Kota dengan Transaksi Terbanyak
st.write("")
st.write("")
st.write("")
st.subheader("Top 5 Kota Berdasarkan Jumlah Transaksi")
top_city_transactions = top_city_transaction_df.head(5)
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#72BCD4" if i == 0 else "#D3D3D3" for i in range(len(top_city_transactions))]
ax.barh(
    top_city_transactions["customer_city"],
    top_city_transactions["transaction_amount"],
    color=colors,
)
ax.set_title("Top 5 Kota Berdasarkan Jumlah Transaksi")
ax.invert_yaxis()
st.pyplot(fig)
with st.expander("Kota mana yang memiliki jumlah transaksi terbanyak berdasarkan data pelanggan?"):
    st.write("""
                Berdasarkan visualisasi diatas diketahui bahwa **Sao Paulo** memiliki jumlah transaksi yang jauh lebih tinggi dibandingkan kota lainnya, menunjukkan bahwa kota ini adalah pasar utama untuk bisnis e-commerce. Hal ini bisa disebabkan oleh populasi yang besar, daya beli yang tinggi, atau infrastruktur e-commerce yang lebih baik maupun kota yang lebih maju.

                Rio de Janeiro berada di posisi kedua, meskipun jumlah transaksinya jauh lebih rendah dibandingkan Sao Paulo. Ini menunjukkan bahwa meskipun Rio de Janeiro memiliki pasar besar, potensinya mungkin belum dimanfaatkan secara maksimal dibandingkan Sao Paulo.

                Sedangkan Belo Horizonte, Brasilia, dan Curitiba, ketiga kota ini menunjukkan jumlah transaksi yang signifikan tetapi masih jauh lebih rendah dibandingkan dua kota teratas.
             """)
st.subheader("Tabel Lengkap Kota Dengan Jumlah Transaksi Terbanyak")
st.write(top_city_transactions)

st.subheader("Kesimpulan - 1")
st.write("""
            - Jumlah pesanan e-commerce mengalami tren kenaikan dari 2016 hingga akhir 2017, dengan lonjakan besar pada November 2017. Setelah itu, pesanan stabil pada 2018 dengan sedikit fluktuasi, menunjukkan pasar mulai mencapai keseimbangan.
            - Produk bed_bath_table memiliki penjualan tertinggi, diikuti oleh kategori rumah tangga, kecantikan, dan gaya hidup. Sebaliknya, kategori seperti security_and_services, pakaian anak-anak, gaming, dan media fisik memiliki penjualan yang sangat rendah, menunjukkan permintaan yang lebih kecil.
            - Kartu kredit adalah metode pembayaran yang paling sering digunakan, menunjukkan preferensi pelanggan terhadap transaksi berbasis kartu. Boleto masih memiliki pangsa pasar signifikan, sementara voucher dan debit card kurang diminati.
            - Sao Paulo mendominasi jumlah transaksi e-commerce, diikuti oleh Rio de Janeiro dengan selisih yang besar. Kota lain seperti Belo Horizonte, Brasília, dan Curitiba menunjukkan potensi pertumbuhan lebih lanjut.
        """)

# Analisis Lanjutan
st.write("")
st.write("")
st.write("")
st.subheader("Analisis Lanjutan")
fig = px.scatter_mapbox(
    geo_customer_distribution_df,
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
    st.text("""
                Tampilan diatas adalah tampilan dari Scatter Mapbox dari distribusi transaksi yang terdapat di Brazil berdasarkan pelanggan.
                
                Sebagian besar pelanggan terkonsentrasi di wilayah tenggara dan timur Brazil, terutama di sekitar kota besar seperti São Paulo, Rio de Janeiro, dan Belo Horizonte.
                
                Banyaknya pelanggan di wilayah tersebut dapat didasari oleh pusat ekonomi dan bisnis maupun kemajuan dari kota tersebut.
            """)

st.write("")
st.write("")
st.write("")
fig_map = px.scatter_mapbox(
    geo_top_city_transaction_df,
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
fig_map.update_layout(
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=50, b=0)
)
st.plotly_chart(fig_map)
with st.expander("Insight - Geoanalysis Kota dengan Pelanggan Terbanyak"):
    st.text("""
                Dapat dilihat berdasarkan Scatter Mapbox diatas bahwa warna (semakin gelap) dan ukuran titik (semakin besar) menunjukkan jumlah transaksi dengan Kota São Paulo memiliki transaksi terbesar dibandingkan kota lainnya.
            
                Meskipun tidak sebesar Kota São Paulo, dapat dilihat pula bahwa Kota Rio de Janeiro juga menunjukkan jumlah transaksi yang cukup tinggi.
            """)

st.subheader("Kesimpulan - 2")
st.write("""
            - Sebaran transaksi e-commerce di Brazil paling banyak terkonsentrasi di wilayah tenggara dan timur, terutama di kota-kota besar seperti São Paulo, Rio de Janeiro, dan Belo Horizonte. Hal ini kemungkinan dipengaruhi oleh faktor ekonomi, bisnis, dan perkembangan infrastruktur di daerah tersebut.

            - Kota São Paulo memiliki jumlah transaksi tertinggi dibandingkan kota lain, dengan ukuran dan warna titik yang lebih mencolok. Sementara itu, Kota Rio de Janeiro juga menunjukkan aktivitas transaksi yang cukup tinggi, meskipun tidak sebesar São Paulo.
        """)

with st.sidebar:
    st.markdown("<h3 style='text-align: center;'> 🔗 GitHub Repository</h3>", unsafe_allow_html=True)
    github_logo_url = "https://cdn-icons-png.flaticon.com/512/25/25231.png"
    repo_url = "https://github.com/daffarayhanriadi/ecommerce-data-analysis"
    st.markdown(f"""
                    <div style="display: flex; justify-content: center;">
                        <a href="{repo_url}" target="_blank">
                            <img src="{github_logo_url}" width="70">
                        </a>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader(":bar_chart: Data Source")
    st.markdown("""
                    :link: [**Brazilian E-Commerce Dataset**](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
                    *Explore real-world e-commerce transactions in Brazil!*
                """)
    st.markdown("---")
    st.markdown("""
                    :pushpin: **Created by:** Daffa Rayhan Riadi  
                    :e-mail: **Contact:** [Email](mailto:daffarayhanriadi@gmail.com)  
                """)

st.markdown("---")
st.caption("Copyright © 2025 | Daffa Rayhan Riadi - Laskar AI | Passionate in Data Analytics & Artificial Intelligence")