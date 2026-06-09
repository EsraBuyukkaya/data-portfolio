# FIFA World Cup Team Popularity & Player Earnings Analysis

Notebook-style exploratory data analysis inspired by a classic data analyst portfolio format: questions, data wrangling, exploratory analysis, and conclusions.

## Scenario

A sports media team wants a clear, data-backed story before publishing a World Cup feature. The team wants to know which countries dominate tournament history, which teams are most visible to global fans, and whether the highest-paid footballers come from the most successful World Cup nations.

## Questions Answered

- Which countries have won the FIFA World Cup the most?
- Which countries reach finals most often?
- Which teams look most "popular" using a measurable World Cup visibility score?
- Which regions dominate World Cup titles?
- Do the highest-paid footballers come from countries with strong World Cup records?

## Data Sources

- FIFA World Cup winners and finalists: public FIFA historical summaries for champions from 1930-1978 and 1982-2022.
- World Cup title counts and tournament history: FIFA World Cup historical records.
- Highest-paid player earnings: Forbes 2025 highest-paid soccer player estimates.

## Important Note

"Most popular teams" is measured as a **visibility proxy**, not a fan survey. The score rewards titles, finals, and tournament appearances:

```text
visibility_score = titles * 5 + finals * 3 + appearances
```

That choice makes the analysis more honest because popularity can mean many things: global fanbase, social media, jersey sales, TV ratings, or tournament success.

## Tools

- Python
- Pandas
- Jupyter Notebook
- CSV data modeling

## Portfolio Skills Demonstrated

- Exploratory data analysis
- Data cleaning and standardization
- Business question framing
- Metric design
- Joining sports performance and compensation datasets
- Clear written findings for non-technical readers

## Project Files

- `World_Cup_Football_Analysis.ipynb` - main notebook
- `data/world_cup_editions.csv` - World Cup winners and runners-up
- `data/team_summary.csv` - team-level appearances, titles, finals, and regions
- `data/highest_paid_players_2025.csv` - Forbes-based player earnings dataset
- `src/analyze_world_cup.py` - reproducible analysis script

## Key Findings

- Brazil leads World Cup history with 5 titles.
- Germany has one of the strongest consistency profiles, with 4 titles and the most final appearances in this dataset.
- Argentina, France, and Brazil are especially strong modern-era teams.
- The highest-paid players are not always from the countries with the most World Cup titles, which shows the difference between individual market value, league economics, and national team dominance.
- The visibility score puts Brazil, Germany, Argentina, Italy, and France near the top because they combine titles, finals, and repeated tournament appearances.
