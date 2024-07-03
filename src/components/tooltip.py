import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback

# Mapping for attribute-tt values to markdown texts
attribute_tooltips = {
    #PAS things
    'PAS-Confidence': (
        '### PAS-Confidence\n\n'
        'Confidence reflects the level of trust, assurance, and belief in the capabilities and actions of local authorities, including law enforcement agencies, justice institutions, and community leaders. It encompasses perceptions of competence, responsiveness, and effectiveness in addressing community needs and concerns.\n\n'
        '**"Good Job" Local**\n\n'
        'This assesses the perception of the quality of work and performance of local authorities in addressing community issues, maintaining public safety, and delivering services. It reflects community members\' confidence in the ability of local authorities to effectively fulfill their responsibilities and achieve positive outcomes.\n\n'
        '**Informed Local**\n\n'
        'This reflects the extent to which community members feel adequately informed and engaged by local authorities regarding important issues, policies, programs, and decisions affecting the community. It involves transparent communication, accessibility of information, and opportunities for meaningful participation and input from community members.\n\n'
        '**Listen to Concerns**\n\n'
        'This aspect assesses the extent to which local authorities actively listen, acknowledge, and respond to the concerns, needs, and perspectives of community members. It involves open communication channels, empathy, and responsiveness to community input, feedback, and grievances.\n\n'
        '**Relied on to Be There**\n\n'
        'This mirrors the trust dimension and reflects the perception of reliability and dependability of local authorities in being present, responsive, and available to address community needs, emergencies, and crises. It involves confidence in the accessibility and responsiveness of local authorities in ensuring public safety and providing assistance and support.\n\n'
        '**Understand Issues**\n\n'
        'This evaluates the level of understanding, awareness, and sensitivity of local authorities to the diverse issues, challenges, and priorities facing the community. It involves efforts to empathize, educate, and address the underlying causes of community problems, including social, economic, and cultural factors.'
    ),
    'Trust': (
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
    ),
    #Economic
    'Economic-Industry': (
        '### Industry Type\n\n'
        'This category includes the type of industry in which the defendants are employed at the time of their prosecution.\n\n'
        '**Manufacturing**:\n\n'
        'Includes defendants employed in industries involved in the production of goods, such as factories and assembly lines.\n\n'
        '**Construction**:\n\n'
        'Encompasses defendants working in the construction sector, including roles in building, civil engineering, and related trades.\n\n'
        '**Hotels and Restaurants**:\n\n'
        'Covers defendants working in the hospitality industry, including positions in hotels, restaurants, cafes, and bars.\n\n'
        '**Transport and Communication**:\n\n'
        'Includes defendants employed in transportation services (e.g., public transit, shipping, logistics) and communication sectors (e.g., telecommunications, postal services).\n\n'
        '**Banking, Insurance, and Finance**:\n\n'
        'Encompasses defendants working in financial services, including banks, insurance companies, investment firms, and other financial institutions.\n\n'
        '**Public Administration, Education, and Health**:\n\n'
        'Covers defendants employed in government services, educational institutions, healthcare providers, and related public services.'
    ),
    'Economic-Demographic': (
        '### Ethnicity\n\n'
        'This category includes the ethnic background of the defendants involved in criminal cases. Understanding the distribution of ethnicity among defendants can provide valuable insights into potential disparities, trends, and the effectiveness of justice administration across different ethnic groups.'
    ),
    'Economic-Employment': (
        '## Economic Employment: \n\n'
        '**Economically Inactive (Percentage)**\n\n'
        'Economically inactive measures the proportion of defendants who are economically inactive (active:inactive) '
        'out of the total number of defendants prosecuted. Economically inactive individuals are those who are not engaged '
        'in paid employment or self-employment and are not actively seeking work. This can include people who are retired, '
        'students, homemakers, disabled, or otherwise not participating in the labor force. \n\n'
        '**Job Density**\n\n'
        'Job density is a measure that indicates the number of jobs available relative to the population within a specific '
        'area or among a particular group, such as defendants. Higher job density generally suggests better employment '
        'opportunities, while lower job density may indicate fewer available jobs and potentially higher unemployment rates. \n\n'
        '**Employment Type**\n\n'
        'The employment type measures the employment status of defendants, focusing on different aspects of their employment '
        'such as whether they are self-employed, working full-time or part-time, and the gender breakdown of these employment '
        'types. The focus is on the working-age population, which typically includes individuals aged 16-64.'
    ),

    #Stop and Search

    'SS-Age': (
        '### Age\n\n'
        'This category includes the age of the defendants at the time of their prosecution. Age can be an important factor '
        'in understanding trends and patterns in criminal behavior, as well as in tailoring appropriate interventions and sentencing.'
    ),
    'SS-Ethnicity': (
        '### Ethnicity\n\n'
        'This category includes the ethnic background of the defendants involved in criminal cases. Understanding the distribution '
        'of ethnicity among defendants can provide valuable insights into potential disparities, trends, and the effectiveness of '
        'justice administration across different ethnic groups.'
    ),
    'SS-Object': (
        '### Reason of Stop-and-Search\n\n'
        '**Drugs:**\n\n'
        'Cases where individuals are stopped and searched due to suspicion of possessing, using, or distributing illegal drugs. '
        'This type of search aims to prevent drug-related crimes and remove illegal substances from circulation.\n\n'
        '**Other:**\n\n'
        'Cases where individuals are stopped and searched for reasons other than drug-related suspicions. This can include suspicion '
        'of carrying weapons, stolen property, involvement in violent crimes, or other illegal activities. These searches are conducted '
        'to maintain public safety and prevent various types of criminal behavior.'
    ),
    'SS-Outcome': (
        '### Outcomes\n\n'
        '**Not guilty:**\n\n'
        'A verdict indicating that the prosecution failed to meet the burden of proof required to convict the defendant. '
        '*(variable not-guilty of the dataset)*\n\n'

        '**Awaiting outcome:**\n\n'
        'This category encompasses cases that are still in progress or where the final decision has not yet been made. '
        'The following attributes are included in this category:\n\n'

        '- **Status-update-unavailable**: Cases where there is no recent information or update available regarding the current status.\n'
        '- **Under-investigation**: Cases that are actively being examined by authorities, with evidence and details still being gathered or reviewed.\n'
        '- **Unable-to-proceed**: Cases that cannot move forward at the moment due to various reasons such as lack of evidence, legal obstacles, or procedural issues.\n'
        '- **Court-result-unavailable**: Cases where the court\'s decision or verdict has not yet been made public or is pending.\n'
        '- **Awaiting-court-result**: Cases that have been heard by the court, but the final decision or verdict has not yet been rendered.\n\n'

        '**Penalty notice:**\n\n'
        'This category comprises cases where individuals are subject to formal warnings or notices, providing immediate and often '
        'less severe consequences for their actions while avoiding the need for extensive legal proceedings.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Drugs-possession-warning**: Cases where individuals found in possession of a small quantity of drugs receive a formal warning instead of facing prosecution. '
        'This warning serves as a deterrent and an opportunity for the individual to avoid further legal consequences if they comply with the law.\n'
        '- **Penalty-notice-issued**: Cases where individuals are issued a penalty notice, often for minor offenses such as public disorder, minor theft, or traffic violations. '
        'The notice includes a fine that must be paid, serving as an immediate financial penalty without the need for court proceedings.\n'
        '- **Cautioned**: Cases where individuals receive a formal caution from the police. This is a recorded warning that, while not a conviction, '
        'remains on the individual\'s record and can influence future legal proceedings. It is typically used for first-time or minor offenses and aims to deter repeat behavior.\n\n'

        '**Fined:**\n\n'
        'This includes cases where individuals have been assigned non-custodial sentences that involve financial penalties, community service, or conditional measures.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Fined**: Cases where a monetary penalty has been imposed as punishment for the offense. This serves as a financial deterrent and reparation for the wrongdoing.\n'
        '- **Compensation**: Cases where the offender is required to pay a specified amount to the victim as restitution for the harm caused. '
        'This aims to financially compensate the victim for their losses.\n'
        '- **Community-penalty**: Cases where the offender is ordered to perform a certain number of hours of community service. '
        'This serves as a way to give back to the community and rehabilitate the offender through constructive work.\n'
        '- **Conditional-discharge**: Cases where the offender is released under specific conditions without immediate penalty. If the offender meets these conditions, '
        'they avoid further punishment; if not, they may face additional consequences. This acts as a deterrent while giving the offender a chance to reform.\n\n'

        '**Prison sentence:**\n\n'
        'This includes cases where individuals face incarceration or legal charges that could lead to imprisonment. It also encompasses cases with conditional terms related to incarceration.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Imprisoned**: Cases where individuals have been sentenced to serve time in prison as a consequence of their actions. '
        'This represents a custodial sentence where the offender is deprived of their freedom for a specified period.\n'
        '- **Charged**: Cases where individuals have been formally accused of a crime and are awaiting trial. '
        'Being charged indicates that there is sufficient evidence to bring the case to court, where the outcome could potentially result in imprisonment.\n'
        '- **Suspended-sentence**: Cases where individuals receive a prison sentence that is not immediately enforced. '
        'Instead, the sentence is suspended under specific conditions, meaning the offender does not go to prison unless they violate the terms of the suspension. '
        'This serves as a deterrent and an opportunity for rehabilitation without immediate incarceration.'
    ),

    #StreetCrime
    'SC-Outcome': (
        '### Outcomes\n\n'
        '**Not guilty:**\n\n'
        'A verdict indicating that the prosecution failed to meet the burden of proof required to convict the defendant. '
        '*(variable not-guilty of the dataset)*\n\n'

        '**Awaiting outcome:**\n\n'
        'This category encompasses cases that are still in progress or where the final decision has not yet been made. '
        'The following attributes are included in this category:\n\n'

        '- **Status-update-unavailable**: Cases where there is no recent information or update available regarding the current status.\n'
        '- **Under-investigation**: Cases that are actively being examined by authorities, with evidence and details still being gathered or reviewed.\n'
        '- **Unable-to-proceed**: Cases that cannot move forward at the moment due to various reasons such as lack of evidence, legal obstacles, or procedural issues.\n'
        '- **Court-result-unavailable**: Cases where the court\'s decision or verdict has not yet been made public or is pending.\n'
        '- **Awaiting-court-result**: Cases that have been heard by the court, but the final decision or verdict has not yet been rendered.\n\n'

        '**Penalty notice:**\n\n'
        'This category comprises cases where individuals are subject to formal warnings or notices, providing immediate and often '
        'less severe consequences for their actions while avoiding the need for extensive legal proceedings.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Drugs-possession-warning**: Cases where individuals found in possession of a small quantity of drugs receive a formal warning instead of facing prosecution. '
        'This warning serves as a deterrent and an opportunity for the individual to avoid further legal consequences if they comply with the law.\n'
        '- **Penalty-notice-issued**: Cases where individuals are issued a penalty notice, often for minor offenses such as public disorder, minor theft, or traffic violations. '
        'The notice includes a fine that must be paid, serving as an immediate financial penalty without the need for court proceedings.\n'
        '- **Cautioned**: Cases where individuals receive a formal caution from the police. This is a recorded warning that, while not a conviction, '
        'remains on the individual\'s record and can influence future legal proceedings. It is typically used for first-time or minor offenses and aims to deter repeat behavior.\n\n'

        '**Fined:**\n\n'
        'This includes cases where individuals have been assigned non-custodial sentences that involve financial penalties, community service, or conditional measures.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Fined**: Cases where a monetary penalty has been imposed as punishment for the offense. This serves as a financial deterrent and reparation for the wrongdoing.\n'
        '- **Compensation**: Cases where the offender is required to pay a specified amount to the victim as restitution for the harm caused. '
        'This aims to financially compensate the victim for their losses.\n'
        '- **Community-penalty**: Cases where the offender is ordered to perform a certain number of hours of community service. '
        'This serves as a way to give back to the community and rehabilitate the offender through constructive work.\n'
        '- **Conditional-discharge**: Cases where the offender is released under specific conditions without immediate penalty. If the offender meets these conditions, '
        'they avoid further punishment; if not, they may face additional consequences. This acts as a deterrent while giving the offender a chance to reform.\n\n'

        '**Prison sentence:**\n\n'
        'This includes cases where individuals face incarceration or legal charges that could lead to imprisonment. It also encompasses cases with conditional terms related to incarceration.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Imprisoned**: Cases where individuals have been sentenced to serve time in prison as a consequence of their actions. '
        'This represents a custodial sentence where the offender is deprived of their freedom for a specified period.\n'
        '- **Charged**: Cases where individuals have been formally accused of a crime and are awaiting trial. '
        'Being charged indicates that there is sufficient evidence to bring the case to court, where the outcome could potentially result in imprisonment.\n'
        '- **Suspended-sentence**: Cases where individuals receive a prison sentence that is not immediately enforced. '
        'Instead, the sentence is suspended under specific conditions, meaning the offender does not go to prison unless they violate the terms of the suspension. '
        'This serves as a deterrent and an opportunity for rehabilitation without immediate incarceration.'
    ),
    'CrimeOutcomes': (
        '### Outcomes\n\n'
        '**Not guilty:**\n\n'
        'A verdict indicating that the prosecution failed to meet the burden of proof required to convict the defendant. '
        '*(variable not-guilty of the dataset)*\n\n'

        '**Awaiting outcome:**\n\n'
        'This category encompasses cases that are still in progress or where the final decision has not yet been made. '
        'The following attributes are included in this category:\n\n'

        '- **Status-update-unavailable**: Cases where there is no recent information or update available regarding the current status.\n'
        '- **Under-investigation**: Cases that are actively being examined by authorities, with evidence and details still being gathered or reviewed.\n'
        '- **Unable-to-proceed**: Cases that cannot move forward at the moment due to various reasons such as lack of evidence, legal obstacles, or procedural issues.\n'
        '- **Court-result-unavailable**: Cases where the court\'s decision or verdict has not yet been made public or is pending.\n'
        '- **Awaiting-court-result**: Cases that have been heard by the court, but the final decision or verdict has not yet been rendered.\n\n'

        '**Penalty notice:**\n\n'
        'This category comprises cases where individuals are subject to formal warnings or notices, providing immediate and often '
        'less severe consequences for their actions while avoiding the need for extensive legal proceedings.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Drugs-possession-warning**: Cases where individuals found in possession of a small quantity of drugs receive a formal warning instead of facing prosecution. '
        'This warning serves as a deterrent and an opportunity for the individual to avoid further legal consequences if they comply with the law.\n'
        '- **Penalty-notice-issued**: Cases where individuals are issued a penalty notice, often for minor offenses such as public disorder, minor theft, or traffic violations. '
        'The notice includes a fine that must be paid, serving as an immediate financial penalty without the need for court proceedings.\n'
        '- **Cautioned**: Cases where individuals receive a formal caution from the police. This is a recorded warning that, while not a conviction, '
        'remains on the individual\'s record and can influence future legal proceedings. It is typically used for first-time or minor offenses and aims to deter repeat behavior.\n\n'

        '**Fined:**\n\n'
        'This includes cases where individuals have been assigned non-custodial sentences that involve financial penalties, community service, or conditional measures.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Fined**: Cases where a monetary penalty has been imposed as punishment for the offense. This serves as a financial deterrent and reparation for the wrongdoing.\n'
        '- **Compensation**: Cases where the offender is required to pay a specified amount to the victim as restitution for the harm caused. '
        'This aims to financially compensate the victim for their losses.\n'
        '- **Community-penalty**: Cases where the offender is ordered to perform a certain number of hours of community service. '
        'This serves as a way to give back to the community and rehabilitate the offender through constructive work.\n'
        '- **Conditional-discharge**: Cases where the offender is released under specific conditions without immediate penalty. If the offender meets these conditions, '
        'they avoid further punishment; if not, they may face additional consequences. This acts as a deterrent while giving the offender a chance to reform.\n\n'

        '**Prison sentence:**\n\n'
        'This includes cases where individuals face incarceration or legal charges that could lead to imprisonment. It also encompasses cases with conditional terms related to incarceration.\n\n'

        'The following attributes are included in this category:\n\n'

        '- **Imprisoned**: Cases where individuals have been sentenced to serve time in prison as a consequence of their actions. '
        'This represents a custodial sentence where the offender is deprived of their freedom for a specified period.\n'
        '- **Charged**: Cases where individuals have been formally accused of a crime and are awaiting trial. '
        'Being charged indicates that there is sufficient evidence to bring the case to court, where the outcome could potentially result in imprisonment.\n'
        '- **Suspended-sentence**: Cases where individuals receive a prison sentence that is not immediately enforced. '
        'Instead, the sentence is suspended under specific conditions, meaning the offender does not go to prison unless they violate the terms of the suspension. '
        'This serves as a deterrent and an opportunity for rehabilitation without immediate incarceration.'
    ),
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
    Input('attribute', 'data')
)
def update_markdown_text(data):
    print("tooltip", data)
    return attribute_tooltips.get(data, "")
