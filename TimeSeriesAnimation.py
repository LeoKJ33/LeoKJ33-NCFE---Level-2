import matplotlib.pyplot as plt
import pandas as pd
import statistics as st
import plotly.graph_objects as go

# Load data
BTC = pd.read_csv("HistoricalData_BTC.csv")
SP500 = pd.read_csv("HistoricalData_S&P500.csv")

# Clean and prepare data
BTC.dropna(axis=1, inplace=True)

BTC["Date"] = pd.to_datetime(BTC["Date"])
BTC["Close"] = BTC["Close/Last"].astype(float)
SP500["Date"] = pd.to_datetime(SP500["Date"])
SP500["Close"] = SP500["Close/Last"].astype(float)

# Align datasets to common start date
start_date = max(BTC["Date"].min(), SP500["Date"].min())
print(start_date)

BTC = BTC[BTC["Date"] >= start_date].sort_values('Date', ascending=True).reset_index(drop=True)
SP500 = SP500[SP500["Date"] >= start_date].sort_values('Date', ascending=True).reset_index(drop=True)

# Normalize prices to 100 at start
BTC["Normalized"] = (BTC["Close"] / BTC["Close"].iloc[0]) * 100
SP500["Normalized"] = (SP500["Close"] / SP500["Close"].iloc[0]) * 100

# Calculate statistics
modeBTC = st.mode(BTC["Close"])
modeSP500 = st.mode(SP500["Close"])
medianBTC = st.median(BTC["Close"])
medianSP500 = st.mode(SP500["Close"])

print(f"Modal price(BTC): ${modeBTC}, Modal price(S&P 500): ${modeSP500}")
print(f"Median price(BTC): ${medianBTC}, Median price(S&P 500): ${medianSP500}")
print(f"BTC:\n{BTC.describe()}")
print(f"S&P 500:\n{SP500.describe()}")

# Create static matplotlib plot
plt.figure(figsize=(12, 6))
plt.plot(BTC["Date"], BTC["Normalized"], label="BTC", color="orange")
plt.plot(SP500["Date"], SP500["Normalized"], label="S&P 500", color="blue")
plt.title("BTC vs S&P 500 - Normalized Performance")
plt.ylabel("Normalized Price (%)")
plt.xlabel("Date")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Create interactive Plotly animation
BTCvSP500 = go.Figure()

# Add traces
BTCvSP500.add_trace(go.Scatter(
    x=BTC['Date'],
    y=BTC['Normalized'],
    name='BTC',
    line=dict(color='orange')
))
BTCvSP500.add_trace(go.Scatter(
    x=SP500['Date'],
    y=SP500['Normalized'],
    name='S&P 500',
    line=dict(color='blue')
))

# Create animation frames
frames = []
for i in range(len(BTC)):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=BTC['Date'][:i+1], y=BTC['Normalized'][:i+1]),
            go.Scatter(x=SP500['Date'][:i+1], y=SP500['Normalized'][:i+1])
        ],
        name=f'frame_{i}'
    ))

BTCvSP500.frames = frames

# Update layout with animation controls
BTCvSP500.update_layout(
    title='BTC vs S&P 500 - Normalized Performance',
    xaxis_title='Date',
    yaxis_title='Normalized Price (%)',
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 50, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Pause",
                "method": "animate",
                "args": [[None], {
                    "frame": {"duration": 0, "redraw": True},
                    "mode": "immediate"
                }]
            }
        ]
    }],
    sliders=[{
        "steps": [
            {
                "args": [[f"frame_{i}"], {
                    "frame": {"duration": 0, "redraw": True},
                    "mode": "immediate"
                }],
                "label": BTC['Date'].iloc[i].strftime('%Y-%m-%d'),
                "method": "animate"
            }
            for i in range(0, len(BTC), max(1, len(BTC)//50))
        ]
    }]
)

# Save and display animation
BTCvSP500.write_html("btc_vs_sp500_animation.html")
print("Animation saved as btc_vs_sp500_animation.html - open in browser")
BTCvSP500.show()
