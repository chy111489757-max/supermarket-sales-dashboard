# Supermarket Sales & Operations Dashboard

## 1. Problem & User
This interactive tool is designed for small independent retail store managers and operations teams. It helps them monitor daily sales trends across different product categories, evaluate profitability, and understand basic customer purchasing behavior to support daily operational decisions, such as inventory adjustments and promotional planning.

## 2. Data
The dataset used is the "Supermarket Sales Dataset" sourced from Kaggle. It contains historical sales records including transaction dates, specific purchase times, product lines, gross income, and customer types.
* **Accessed on:** 2025
* **Source:** [Kaggle - Supermarket Sales Dataset](https://www.kaggle.com/datasets/akashbommidi/super-market-sales)

## 3. Methods
The project uses Python to process the raw dataset and Streamlit to build the interactive interface. Key steps include:
* **Data Cleaning & Aggregation:** Using `pandas` to convert text-based dates into standard datetime objects, and grouping data to calculate revenue, margins, and average customer spending.
* **Advanced Visualization:** Integrating **Plotly** to render dynamic, smooth-line trend charts with hover details and custom transparent backgrounds.
* **Multi-dimensional Interaction:** Building an interactive sidebar that allows users to cross-filter data simultaneously by product category, core metrics (quantity/revenue/profit), and customer type.
* **UI/UX Design:** Injecting custom CSS to create a modern "frosted glass" card layout, incorporating a high-quality background and the professional 'Nunito' font for better readability.

## 4. Key Findings & Recommendations
* **Core Revenue Driver:** "Food and beverages" is the absolute core driver of the business, generating the highest total revenue (56,144.84) and gross income (2,673.56). 
  * *Actionable Insight:* Use these high-traffic items for bundle sales to help move slower inventory.
* **Underperforming Segment:** The "Health and beauty" segment underperforms, showing the lowest revenue and profit. 
  * *Actionable Insight:* Implement targeted promotions or set up a dedicated discount area at the checkout.
* **Pricing Strategy:** The data indicates a strictly uniform markup strategy across the store. The gross margin remains fixed at approximately 4.76% for all product lines. 
  * *Actionable Insight:* To increase absolute profit, the store must focus primarily on driving overall sales volume rather than relying on high-margin specialty items.
* **Membership Impact:** The membership program shows a positive but limited impact. Members exhibit a slightly higher average spend per transaction ($327.79) compared to normal customers ($318.12). 
  * *Actionable Insight:* Restructure the membership rewards (e.g., double points for high-value orders) to encourage larger basket sizes.

## 5. How to Run
To run this application locally, ensure you have Python installed. 
1. Clone or download this repository to your local machine.
2. Open your terminal and navigate to the project folder.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt

4. Start the Streamlit application by running:
      ```bash
      streamlit run app.py
      ```

## 6. Demo
* **Demo Video Path:** [about the product\3. demo video.mp4]
* **Source Code Link:** [https://github.com/chy111489757-max/supermarket-sales-dashboard/releases/tag/v1.0.0]

## 7. Limitations & Next Steps
While this dashboard provides valuable insights, there are several areas for future enhancement:
* **Static Data Dependency:** The current tool relies on a static historical dataset and does not account for external real-time factors like seasonal variations, holidays, or sudden supply chain disruptions. 
* **Real-time POS Integration:** A logical next step is integrating a live Point-of-Sale (POS) database API to enable real-time data synchronization and tracking.
* **Automated Inventory Alerts:** Future versions could include a dynamic alert system that automatically notifies the store manager when the inventory of fast-moving goods falls below a safe threshold.
