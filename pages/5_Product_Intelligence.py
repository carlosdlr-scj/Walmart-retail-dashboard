
import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, setup, kpi_row

df = load_data()
f = apply_filters(df)
setup("Product Intelligence", "Which products and categories create or destroy value?")

products = f["Product Name"].nunique()
categories = f["Product Category"].nunique()
subcategories = f["Product Sub-Category"].nunique()
profit = f["Profit"].sum()

kpi_row([
    ("Products", f"{products:,.0f}", "Distinct product names"),
    ("Categories", f"{categories:,.0f}", "Product categories"),
    ("Sub-Categories", f"{subcategories:,.0f}", "Product sub-categories"),
    ("Total Profit", f"${profit/1e6:.2f}M", "Selected period"),
])

prod = f.groupby(["Product Name","Product Category"], as_index=False).agg(
    Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")
)
prod["Profit Margin"] = prod["Profit"]/prod["Sales"]

c1, c2 = st.columns(2)
with c1:
    st.subheader("Top 10 Products by Profit")
    top = prod.nlargest(10, "Profit").sort_values("Profit")
    st.plotly_chart(px.bar(top, x="Profit", y="Product Name", orientation="h", text_auto=".3s"),
                    use_container_width=True)
with c2:
    st.subheader("Bottom 10 Products by Profit")
    bottom = prod.nsmallest(10, "Profit").sort_values("Profit")
    st.plotly_chart(px.bar(bottom, x="Profit", y="Product Name", orientation="h", text_auto=".3s"),
                    use_container_width=True)

st.subheader("Category Performance")
summary = f.groupby("Product Category", as_index=False).agg(
    Sales=("Sales","sum"), Profit=("Profit","sum"),
    Orders=("Order ID","nunique"), Discount=("Discount","mean")
)
summary["Profit Margin"] = summary["Profit"]/summary["Sales"]
st.dataframe(
    summary.sort_values("Profit", ascending=False),
    use_container_width=True, hide_index=True
)
