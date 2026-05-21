# 🤖 Agentic Campaign Optimization Engine

A workshop demonstration of how **AI Agents** can autonomously analyze marketing data, identify poor-performing campaigns, rewrite ad copy, and reallocate budgets in real-time.

## 📋 Overview

This Streamlit application simulates an intelligent marketing agent that continuously monitors campaign performance and takes autonomous actions to optimize results. It's designed as an educational tool to show how AI can transform marketing operations.

### Key Features

- **📊 Campaign Dashboard:** Real-time visualization of marketing performance across platforms and segments
- **🚨 Anomaly Detection:** Automatic identification of underperforming audience segments
- **✏️ Creative Optimization:** AI-powered generation of new ad copy tailored to specific segments
- **💰 Budget Reallocation:** Intelligent reallocation of spend from underperformers to high performers

## 🏗️ Project Structure

```
agentic_campaign_optimizer/
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── data/
│   └── generate_data.py             # Dummy data generation script
│
├── pages/
│   ├── 01_campaign_dashboard.py     # Campaign performance dashboard
│   ├── 02_anomaly_detection.py      # Underperformer identification
│   ├── 03_creative_optimization.py  # AI creative generation
│   └── 04_budget_reallocation.py    # Budget optimization engine
│
└── utils/
    ├── __init__.py                  # Package initialization
    └── analysis.py                  # Core analysis functions
```

## 📊 Data Structure

The application works with marketing campaign data containing:

### Raw Columns
- `Campaign_ID`: Unique campaign identifier
- `Date`: Campaign date
- `Platform`: Meta, Google, or LinkedIn
- `Audience_Segment`: Target demographic segment
- `Ad_Creative_Name`: Name of the ad creative
- `Spend_USD`: Total ad spend
- `Impressions`: Number of ad impressions
- `Clicks`: Number of clicks
- `Conversions`: Number of conversions
- `Revenue_USD`: Total revenue generated

### Calculated Metrics
- `CTR_Percent`: Click-Through Rate (Clicks / Impressions * 100)
- `CPA_USD`: Cost Per Acquisition (Spend / Conversions)
- `ROAS`: Return on Ad Spend (Revenue / Spend)

### Intentional Underperformers

The dummy data is deliberately skewed with 2 underperforming segments:
- **"Soccer Moms 35-45"**: Low CTR (0.2-0.5%), High CPA ($50+)
- **"Retirees 55-65"**: Very low CTR (0.1-0.4%), Very high CPA ($60+)

These segments demonstrate how the Agent identifies and fixes problems.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agentic_campaign_optimizer
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python data/generate_data.py
```

This creates:
- `marketing_campaign_data.csv` - For use in Streamlit app
- `marketing_campaign_data.xlsx` - For viewing in Excel

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use the App

### 🎯 Page 1: Campaign Dashboard
- View overall performance metrics
- Explore spend vs. conversions by platform
- Analyze segment performance with interactive charts
- Understand the baseline data the Agent monitors

**Key Insight:** This is the data source the Agent uses to make decisions.

### 🚨 Page 2: Anomaly Detection
- See which segments the Agent has flagged as underperformers
- Review severity rankings
- Understand why each segment is underperforming
- See the financial impact of poor performance

**Key Insight:** The Agent automatically identifies segments losing money.

### ✏️ Page 3: Creative Optimization
- Select an underperforming segment
- Click "Run AI Agent Analysis"
- Review the Agent's analysis of why the creative is failing
- See 3 new AI-generated ad copy variants tailored to the segment

**Key Insight:** The Agent uses demographic understanding to generate relevant creative.

### 💰 Page 4: Budget Reallocation
- Compare current vs. recommended budget allocation
- See projected conversions from reallocation
- Review segment-by-segment rationale
- Understand the 30-day implementation plan

**Key Insight:** The Agent optimizes spend allocation using data, not intuition.

## 🧠 The Agent's Decision Logic

### 1. Performance Analysis
```
For each segment:
  IF CPA > $50 OR CTR < 0.5%:
    FLAG as underperformer
    CALCULATE severity score
```

### 2. Creative Generation
```
For underperformer:
  ANALYZE audience values and pain points
  GENERATE 3 ad copy variants
  TAILOR each to segment demographic
```

### 3. Budget Reallocation
```
IDENTIFY top 3 performing segments
IDENTIFY underperformers
MOVE 20% of underperformer budget to top performers
PROJECT impact on total conversions
```

## 🔧 Technical Details

### Key Functions

#### `data/generate_data.py`
- `generate_marketing_data()`: Creates 500+ rows of realistic campaign data
- `save_data_to_excel()`: Exports data to Excel with formatting

#### `utils/analysis.py`
- `load_marketing_data()`: Loads CSV data
- `get_segment_performance()`: Aggregates metrics by audience segment
- `get_platform_performance()`: Aggregates metrics by platform
- `identify_underperformers()`: Flags poor-performing segments
- `simulate_ai_agent_analysis()`: Generates analysis and creative variants
- `calculate_budget_reallocation()`: Calculates optimal budget distribution

### Libraries Used
- **Streamlit**: Interactive web app framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **OpenPyXL**: Excel file handling

## 📊 Performance Thresholds

The Agent uses these thresholds to identify underperformers:

| Metric | Threshold | Impact |
|--------|-----------|--------|
| CPA | > $50 | High cost per acquisition |
| CTR | < 0.5% | Low audience engagement |
| ROAS | < 1.0x | No positive return |

## 💡 Educational Concepts

This workshop demonstrates:

1. **Autonomous Decision Making**: Agents make marketing decisions based on data
2. **Real-Time Optimization**: No waiting for reports; changes happen instantly
3. **Scalable Operations**: Same agent logic scales to 1000s of campaigns
4. **Creative AI**: LLMs can generate marketing copy tailored to segments
5. **Financial Impact**: Clear ROI calculation of optimizations

## 🎓 Workshop Discussion Points

1. **Data Quality**: How would bad data affect Agent decisions?
2. **Segment Fatigue**: What happens if budget keeps flowing to the same segments?
3. **Brand Risk**: Could aggressive optimization damage brand perception?
4. **Privacy**: How do we handle demographic targeting responsibly?
5. **Approval Workflows**: Should Agents have autonomous approval, or require human sign-off?

## 🔮 Production Extensions

In a real system, this Agent would:

1. **Connect to Live APIs**: Pull data from Meta Ads, Google Ads, etc.
2. **Real-Time Deployment**: Instantly adjust bids, budgets, and creative
3. **A/B Testing Loop**: Deploy variants and measure automatically
4. **ML Predictions**: Forecast performance before deployment
5. **Compliance Checks**: Ensure all changes meet brand/legal requirements
6. **Executive Dashboards**: Report actions and ROI to leadership

## 📝 Notes for Workshop Facilitators

### Timing
- Initial setup: 10 minutes
- Data generation: 2 minutes
- App walkthrough: 15-20 minutes
- Discussion & questions: 15-20 minutes

### Key Talking Points
- "This is a simulation, but the logic is real"
- "Show how the Agent identifies problems faster than humans"
- "Highlight the creative generation capability"
- "Emphasize the projected ROI impact"

### Live Demo Flow
1. Start with Dashboard to show data
2. Go to Anomaly Detection to highlight problems
3. Run the Agent in Creative Optimization (dramatic spinner!)
4. Show Budget Reallocation and the conversion lift projection
5. Discuss the "What's next?" implications

## 🐛 Troubleshooting

### "No data found" error
```bash
# Make sure you've run the data generation script
python data/generate_data.py
```

### Streamlit not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port 8501 already in use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed: `pip list`
3. Ensure you're in the correct directory
4. Try deleting cache: `streamlit cache clear`

## 📄 License

This is a workshop demonstration project. Feel free to use, modify, and distribute as needed for educational purposes.

## 🙏 Credits

Created as an educational tool to demonstrate AI agent capabilities in marketing optimization.

---

**Ready to see your Agent in action? Run `streamlit run app.py` and explore!** 🚀
