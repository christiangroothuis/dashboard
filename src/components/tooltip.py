import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback

# Mapping for attribute-tt values to markdown texts
attribute_tooltips = {
    'PAS-Confidence': '### PAS-Confidence\n\nomg PAS',
    'PAS-Trust': (
        '### PAS-Trust\n\n'
        'Trust is a multifaceted concept that encompasses various aspects of interpersonal '
        'relationships and perceptions of reliability, fairness, and responsiveness. In the context '
        'of criminal justice, trust between the community and law enforcement agencies, courts, and '
        'other institutions is crucial for effective crime prevention, law enforcement, and the '
        'administration of justice. The following are key dimensions of trust and their explanations:\n\n'
        '#### Listen to Concerns\n\n'
        'This refers to the extent to which individuals believe that law enforcement agencies and justice institutions are attentive to the concerns, grievances, and needs of the community. It involves active listening, empathy, and responsiveness to the voices and experiences of individuals, including victims, witnesses, and community members.\n\n'
        '#### Relied on to Be There\n\n'
        'This reflects the perception of reliability and dependability of law enforcement agencies and justice institutions. It involves the belief that these entities will be present and available to address community needs, provide assistance, and maintain public safety consistently and effectively.\n\n'
        '#### Treat Everyone Fairly\n\n'
        'This emphasizes the importance of impartiality, equity, and non-discrimination in the interactions and decisions of law enforcement agencies and justice institutions. It involves treating all individuals, regardless of their background, identity, or status, with fairness, respect, and dignity, and ensuring that justice is administered without bias or favoritism.'
    )
}

# Markdown component
tooltip_layout = html.Div(
    [
        html.P(
            [
                "Want to know more about the selected category and the included attributes?",
            ],
            style={"textAlign": "center", "fontStyle": "italic"}  # Center the text, Make the text italic
        ),
        dcc.Markdown(
            id="tooltip-markdown",
            children="Noun: rare, the action or habit of estimating something as worthless.",
            style={"padding": "20px", "border": "none", "backgroundColor": "#fff"}
        ),
    ]
)

# Callback to update the markdown text based on 'attribute-tt'
@callback(
    Output('tooltip-markdown', 'children'),
    Input('attribute-tt', 'data')
)
def update_markdown_text(data):
    return attribute_tooltips.get(data, "Noun: rare, the action or habit of estimating something as worthless.")