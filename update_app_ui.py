"""
update_app_ui.py — Overhauls app.py with dual Light/Dark theme support and Altair charts.
"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Matplotlib chart section with Altair native responsive chart
matplotlib_old_pattern = re.compile(
    r'import matplotlib\.pyplot as plt.*?'
    r'plt\.close\(fig\)',
    re.DOTALL
)

altair_replacement = '''import altair as alt

        chart_data = results[:12]
        names  = [r.name.split("(")[0].strip()[:22] for r in chart_data]
        scores = [r.final_score_pct for r in chart_data]
        tiers  = ["Strong (>=60%)" if s >= 60 else "Moderate (30-60%)" if s >= 30 else "Weak (<30%)" for s in scores]

        df_chart = pd.DataFrame({
            "Candidate": names,
            "Match Score (%)": scores,
            "Tier": tiers,
        })

        alt_chart = (
            alt.Chart(df_chart)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, size=18)
            .encode(
                y=alt.Y("Candidate:N", sort="-x", title=None),
                x=alt.X("Match Score (%):Q", scale=alt.Scale(domain=[0, 100]), title="Match Score (%)"),
                color=alt.Color(
                    "Tier:N",
                    scale=alt.Scale(
                        domain=["Strong (>=60%)", "Moderate (30-60%)", "Weak (<30%)"],
                        range=["#10b981", "#f59e0b", "#ef4444"],
                    ),
                    legend=alt.Legend(orient="bottom", title=None),
                ),
                tooltip=["Candidate", "Match Score (%)", "Tier"],
            )
            .properties(height=max(280, len(names) * 32))
            .configure_view(strokeWidth=0)
            .configure_axis(gridDash=[3, 3])
        )

        st.altair_chart(alt_chart, use_container_width=True)'''

content = matplotlib_old_pattern.sub(altair_replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced Matplotlib with Altair successfully')
