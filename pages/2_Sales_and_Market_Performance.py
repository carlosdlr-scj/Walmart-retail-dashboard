
import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, setup, kpi_row

df = load_data()
f = apply_filters(df)
setup("Sales & Market Performance", "Where does our revenue come from?")

sales = f["Sales"].sum()
orders = f["Order ID"].nunique()
customers = f["Customer Name"].nunique()
aov = sales / orders if orders else 0

kpi_row([
    ("Sales", f"${sales/1e6:.2f}M", "Selected period"),
    ("Orders", f"{orders:,.0f}", "Distinct orders"),
    ("Customers", f"{customers:,.0f}", "Customer names"),
    ("Average Order Value", f"${aov:,.1f}", "Sales / orders"),
])

seg = f.groupby("Customer Segment", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
seg["Profit Margin"] = seg["Profit"]/seg["Sales"]
cat = f.groupby("Product Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
cat["Profit Margin"] = cat["Profit"]/cat["Sales"]

c1, c2 = st.columns(2)
with c1:
    st.subheader("Sales by Customer Segment")
    st.plotly_chart(px.bar(seg.sort_values("Sales"), x="Sales", y="Customer Segment",
                           orientation="h", text_auto=".3s"), use_container_width=True)
with c2:
    st.subheader("Sales by Product Category")
    st.plotly_chart(px.bar(cat.sort_values("Sales"), x="Sales", y="Product Category",
                           orientation="h", text_auto=".3s"), use_container_width=True)

st.subheader("Customer Revenue Concentration")
customer = f.groupby("Customer Name", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
customer["Customer Rank"] = range(1, len(customer)+1)
customer["Cumulative Sales Share"] = customer["Sales"].cumsum()/customer["Sales"].sum()
customer["Cumulative Customer Share"] = customer["Customer Rank"]/len(customer)

fig = px.line(customer, x="Cumulative Customer Share", y="Cumulative Sales Share",
              hover_data=["Customer Name","Sales"])
fig.update_xaxes(tickformat=".0%", title="% of customers")
fig.update_yaxes(tickformat=".0%", title="% of cumulative sales")
fig.add_hline(y=0.8, line_dash="dash")
fig.add_vline(x=0.2, line_dash="dash")
fig.update_layout(height=370)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "This Pareto-style view shows how concentrated revenue is among customers. "
    "The dataset does not contain a Customer ID, so Customer Name is used as the available customer identifier."
)

st.subheader("Sales Trend by Region")
trend = f.groupby(["Month","Region"], as_index=False)["Sales"].sum()
st.plotly_chart(px.line(trend, x="Month", y="Sales", color="Region"), use_container_width=True)
