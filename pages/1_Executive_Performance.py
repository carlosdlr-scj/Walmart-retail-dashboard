
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, apply_filters, setup, kpi_row

df = load_data()
f = apply_filters(df)
setup("Executive Performance", "How is the business performing and is the growth sustainable?")

sales = f["Sales"].sum()
profit = f["Profit"].sum()
margin = profit / sales if sales else 0
orders = f["Order ID"].nunique()
aov = sales / orders if orders else 0

kpi_row([
    ("Profit Margin", f"{margin:.1%}", "North Star Metric"),
    ("Total Sales", f"${sales/1e6:.2f}M", "Selected period"),
    ("Total Profit", f"${profit/1e6:.2f}M", "Selected period"),
    ("Total Orders", f"{orders:,.0f}", "Distinct orders"),
    ("Average Order Value", f"${aov:,.1f}", "Sales / orders"),
])

st.write("")
left, right = st.columns([1.65, 1])

monthly = f.groupby("Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
monthly["Profit Margin"] = monthly["Profit"] / monthly["Sales"]

with left:
    st.subheader("Sales and Profit Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Sales"], mode="lines", name="Sales"))
    fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Profit"], mode="lines", name="Profit"))
    fig.update_layout(height=285, margin=dict(l=10,r=10,t=10,b=10), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Profit Margin Trend")
    fig = px.line(monthly, x="Month", y="Profit Margin")
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Year-over-Year Performance")
    yearly = f.groupby("Year", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
    yearly["Margin"] = yearly["Profit"] / yearly["Sales"]
    yearly["Sales Growth"] = yearly["Sales"].pct_change()
    yearly["Profit Growth"] = yearly["Profit"].pct_change()
    yoy = yearly.melt(id_vars="Year", value_vars=["Sales Growth","Profit Growth","Margin"],
                      var_name="Metric", value_name="Value")
    fig = px.bar(yoy, x="Year", y="Value", color="Metric", barmode="group")
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(height=310, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Reading guide: compare Sales Growth and Profit Growth with Margin to assess sustainable growth.")

st.write("")
c1, c2, c3 = st.columns(3)
region = f.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
region["Margin"] = region["Profit"] / region["Sales"]
cat = f.groupby("Product Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
cat["Margin"] = cat["Profit"] / cat["Sales"]

with c1:
    st.subheader("Performance by Region")
    st.plotly_chart(px.bar(region.sort_values("Sales"), x="Sales", y="Region", orientation="h"),
                    use_container_width=True)
with c2:
    st.subheader("Sales by Category")
    st.plotly_chart(px.bar(cat.sort_values("Sales"), x="Sales", y="Product Category", orientation="h"),
                    use_container_width=True)
with c3:
    st.subheader("Profit Margin by Category")
    fig = px.bar(cat.sort_values("Margin"), x="Margin", y="Product Category", orientation="h")
    fig.update_xaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
