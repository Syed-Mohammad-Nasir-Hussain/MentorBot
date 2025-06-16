import plotly.graph_objects as go

def plot_skill_radar(user_skills, role_skills, role_name):
    categories = list(set(user_skills).union(set(role_skills)))
    categories = sorted(categories)

    user_values = [1 if skill in user_skills else 0 for skill in categories]
    role_values = [1 if skill in role_skills else 0 for skill in categories]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(r=user_values, theta=categories, fill='toself', name='You'))
    fig.add_trace(go.Scatterpolar(r=role_values, theta=categories, fill='toself', name=role_name))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title=f"🕸️ Skill Match Radar — {role_name}"
    )

    return fig
