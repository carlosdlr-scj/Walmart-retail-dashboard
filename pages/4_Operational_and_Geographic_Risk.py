
import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters, setup, kpi_row

df = load_data()
f = apply_filters(df)
setup("Operational & Geographic Risk", "Where do logistics and geography affect profitability?")

f = f.copy()
f["Shipping Days"] = (f["Ship Date"] - f["Order Date"]).dt.days

kpi_row([
    ("Shipping Cost", f"${f['Shipping Cost'].sum():,.0f}", "Selected period"),
    ("Avg. Shipping Cost", f"${f['Shipping Cost'].mean():,.2f}", "Per line item"),
    ("Avg. Shipping Days", f"{f['Shipping Days'].mean():.1f}", "Order to ship"),
    ("Profit Margin", f"{f['Profit'].sum()/f['Sales'].sum():.1%}", "Selected period"),
])

mode = f.groupby("Ship Mode", as_index=False).agg(
    Shipping_Cost=("Shipping Cost","sum"),
    Avg_Shipping_Days=("Shipping Days","mean"),
    Profit=("Profit","sum")
)
c1, c2 = st.columns(2)
with c1:
    st.subheader("Shipping Cost by Ship Mode")
    st.plotly_chart(px.bar(mode, x="Ship Mode", y="Shipping_Cost", text_auto=".3s"),
                    use_container_width=True)
with c2:
    st.subheader("Shipping Cost vs. Profit")
    st.plotly_chart(px.scatter(f, x="Shipping Cost", y="Profit", color="Ship Mode",
                               hover_data=["Order ID","Product Name"]),
                    use_container_width=True)

state = f.groupby("State", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
state["Profit Margin"] = state["Profit"]/state["Sales"]
st.subheader("Profit Margin by State")
st.plotly_chart(px.bar(state.nlargest(15, "Profit Margin").sort_values("Profit Margin"),
                       x="Profit Margin", y="State", orientation="h", text_auto=".1%"),
                use_container_width=True)
