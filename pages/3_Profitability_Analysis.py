
import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, setup, kpi_row

df = load_data()
f = apply_filters(df)
setup("Profitability Analysis", "Which commercial decisions are creating or destroying value?")

sales = f["Sales"].sum()
profit = f["Profit"].sum()
margin = profit/sales if sales else 0
avg_discount = f["Discount"].mean()
shipping = f["Shipping Cost"].sum()

kpi_row([
    ("Total Profit", f"${profit/1e6:.2f}M", "Selected period"),
    ("Profit Margin", f"{margin:.1%}", "North Star Metric"),
    ("Average Discount", f"{avg_discount:.1%}", "Average line-item discount"),
    ("Shipping Cost", f"${shipping/1e6:.2f}M", "Total shipping cost"),
])

st.write("")
st.subheader("Discount vs. Profitability")
st.caption(
    "Reading guide: each point is a discount level. Higher points mean higher profitability; larger bubbles mean more Sales."
)

discount = f.groupby("Discount", as_index=False).agg(
    Sales=("Sales","sum"),
    Profit=("Profit","sum"),
    Orders=("Order ID","nunique")
)
discount["Profit Margin"] = discount["Profit"]/discount["Sales"]

fig = px.scatter(
    discount,
    x="Discount",
    y="Profit Margin",
    size="Sales",
    hover_data=["Sales","Profit","Orders"],
    text=discount["Discount"].map(lambda x: f"{x:.0%}")
)
fig.update_xaxes(tickformat=".0%", title="Discount level")
fig.update_yaxes(tickformat=".0%", title="Profit margin")
fig.update_layout(height=410, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Reading guide: move left to right as discount increases. Focus on levels where margin falls while Sales remain substantial."
)
st.subheader("Product Profitability Matrix")
prod = f.groupby(["Product Name","Product Category"], as_index=False).agg(
    Sales=("Sales","sum"), Profit=("Profit","sum")
)
prod["Profit Margin"] = prod["Profit"]/prod["Sales"]
prod["Bubble Profit"] = prod["Profit"].abs()

fig = px.scatter(
    prod, x="Sales", y="Profit Margin", size="Bubble Profit",
    color="Product Category", hover_name="Product Name",
    hover_data=["Profit","Sales"]
)
fig.update_yaxes(tickformat=".0%", title="Profit margin")
fig.update_layout(height=450)
st.plotly_chart(fig, use_container_width=True)
st.caption("Bubble size uses absolute profit so loss-making products can still be displayed without Plotly size errors.")
