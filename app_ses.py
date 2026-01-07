import streamlit as st
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="Valutazione Self-Empowerment", layout="centered")

    st.title("Valutazione del Livello di Self-Empowerment")
    st.markdown("""
    Questo strumento ti permette di autovalutare il tuo livello di **Self-Empowerment**.
    
    Rispondi alle seguenti affermazioni indicando quanto sei d'accordo con ciascuna di esse.
    Non ci sono risposte giuste o sbagliate, cerca di essere il più sincero possibile.
    """)

    st.write("---")

    # Definizione delle domande e della loro tipologia (Standard o Reverse)
    # Reverse = True significa che "per niente d'accordo" vale 5 invece di 1.
    questions = [
        {"id": 1,  "text": "1. È meglio concentrarsi sul presente, senza fare troppi progetti futuri", "reverse": True},
        {"id": 2,  "text": "2. Generalmente sento di avere molta influenza su ciò che mi accade nel lavoro", "reverse": False},
        {"id": 3,  "text": "3. Se penso alla mia vita professionale, mi sembra che le mie possibilità siano aumentate", "reverse": False},
        {"id": 4,  "text": "4. È meglio restare coi piedi per terra, evitando di avere troppi desideri", "reverse": True},
        {"id": 5,  "text": "5. Generalmente mi è difficile pensarmi in circostanze future", "reverse": True},
        {"id": 6,  "text": "6. Generalmente mi sembra di imparare e di crescere nel lavoro", "reverse": False},
        {"id": 7,  "text": "7. Più uno cresce e più aumentano i vincoli e diminuiscono le possibilità", "reverse": True},
        {"id": 8,  "text": "8. Generalmente mi sembra di realizzare qualcosa di buono con il mio lavoro", "reverse": False},
        {"id": 9,  "text": "9. Viviamo in un mondo ricco di possibilità, anche professionali", "reverse": False},
        {"id": 10, "text": "10. Se penso al mio futuro, mi è facile vedere i miei desideri realizzati", "reverse": False},
        {"id": 11, "text": "11. Se penso alla mia vita professionale, penso di avere molte risorse a disposizione", "reverse": False},
        {"id": 12, "text": "12. Generalmente mi sembra di incidere in ciò che faccio sul lavoro", "reverse": False},
        {"id": 13, "text": "13. Generalmente ritengo di avere diverse possibilità tra cui scegliere", "reverse": False},
    ]

    # Opzioni di risposta
    options_map = {
        "per niente d'accordo": 1,
        "poco d'accordo": 2,
        "né d'accordo né in disaccordo": 3,
        "abbastanza d'accordo": 4,
        "totalmente d'accordo": 5
    }
    
    options_list = list(options_map.keys())
    
    scores = []
    
    # Creazione del form
    with st.form("ses_questionnaire"):
        for q in questions:
            st.markdown(f"**{q['text']}**")
            # Usa una chiave unica per ogni widget
            response = st.radio(
                f"Seleziona la tua risposta per la domanda {q['id']}:",
                options_list,
                index=2, # Default su neutro
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )
            
            # Calcolo del punteggio
            raw_score = options_map[response]
            if q['reverse']:
                # Se è reverse: 1->5, 2->4, 3->3, 4->2, 5->1
                # Formula: 6 - raw_score
                final_score = 6 - raw_score
            else:
                final_score = raw_score
            
            scores.append(final_score)
            st.markdown("---")
        
        submitted = st.form_submit_button("Calcola Risultato")

    if submitted:
        # Calcolo della media
        total_score = sum(scores)
        average_score = total_score / len(scores)

        st.header("Il tuo Risultato")
        
        # Feedback Narrativo
        result_level = ""
        result_color = ""
        
        if average_score <= 3:
            result_level = "BASSO"
            result_color = "red"
            description = "Il punteggio indica una percezione limitata delle proprie possibilità di influenza e scelta nel contesto lavorativo/personale."
        elif average_score <= 4:
            result_level = "MEDIO"
            result_color = "orange"
            description = "Il punteggio indica un livello intermedio di self-empowerment, con un equilibrio tra percezione di vincoli e possibilità."
        else:
            result_level = "ALTO"
            result_color = "green"
            description = "Il punteggio indica un'ottima percezione delle proprie risorse, un senso di agenzia forte e una visione aperta verso il futuro."

        st.markdown(f"### Livello di Self-Empowerment: :{result_color}[{result_level}]")
        st.markdown(f"**Punteggio medio:** {average_score:.2f} / 5.00")
        st.info(description)

        # Feedback Grafico (Gauge Chart)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = average_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Punteggio SES"},
            gauge = {
                'axis': {'range': [1, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': result_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [1, 3], 'color': '#ffcccc'},  # Rosso chiaro
                    {'range': [3, 4], 'color': '#ffedcc'},  # Arancio chiaro
                    {'range': [4, 5], 'color': '#ccffcc'}   # Verde chiaro
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': average_score
                }
            }
        ))
        
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()