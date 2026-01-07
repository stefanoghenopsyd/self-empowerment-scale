import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Tenta di importare la connessione a GSheets
try:
    from streamlit_gsheets import GSheetsConnection
    HAS_GSHEETS = True
except ImportError:
    HAS_GSHEETS = False

def main():
    st.set_page_config(page_title="Self-empowerment Assessment", layout="centered")

    # --- MODIFICA LOGO: CENTRATO E PIÙ GRANDE ---
    try:
        # Creiamo 3 colonne: spazio vuoto (1), logo (3), spazio vuoto (1)
        col_left, col_center, col_right = st.columns([1, 3, 1])
        
        with col_center:
            # width=600 aumenta la dimensione (prima era 200)
            st.image("GENERA Logo Colore.png", width=450) 
    except:
        st.warning("Logo 'GENERA Logo Colore.png' non trovato. Carica il file nella directory dell'app.")
    # ---------------------------------------------

    st.title("Self-Empowerment Assessment")

    # INTRODUZIONE TEORICA
    with st.expander("Cos'è il Self-Empowerment?", expanded=True):
        st.markdown("""
        Il concetto di **Self-Empowerment**, nel modello teorico elaborato da **Massimo Bruscaglioni** e successivamente sviluppato con **Stefano Gheno**, non si riferisce al semplice "potere su" (dominio), ma al **"potere di"**: la capacità di aprire nuove possibilità e di sentirsi protagonisti della propria vita.
        Secondo gli autori (*"Il gusto del potere", 2000*), il processo di self-empowerment si fonda sul passaggio:
        1.  Dal **Bisogno** (mancanza) al **Desiderio** (aspirazione positiva).
        2.  Attraverso la **Pensabilità Positiva**: la capacità di vedere risorse dove prima si vedevano solo vincoli.
        3.  Fino alla **Possibilitazione**: l'apertura concreta di nuove opzioni di scelta.
        > *"L'empowerment è quel processo che permette di passare da una condizione di passività o di reattività, a una di proattività, in cui il soggetto recupera la propria 'agenzia' e la capacità di incidere sul proprio contesto."*
        
        Questo questionario ti aiuta a riflettere su dove ti posizioni oggi rispetto a questa capacità di generare possibilità. Troverai 13 affermazioni, indica il tuo grado di accordo con ciascuna di esse su una scala che va da 1 (per nulla d'accordo) a 5 (totalmente d'accordo). Il test è del tutto anonimo e ti fornira un feedback immediato circa il tuo livello di Self-empowerment.
        """)

    st.write("---")

    # SEZIONE SOCIO-ANAGRAFICA
    st.subheader("Dati Socio-Anagrafici")
    st.markdown("Prima di iniziare, ti chiediamo alcune informazioni statistiche.")
    
    col1, col2 = st.columns(2)
    with col1:
        genere = st.selectbox(
            "Genere",
            ["Seleziona...", "Maschile", "Femminile", "Non binario", "Non risponde"]
        )
    with col2:
        eta = st.selectbox(
            "Fascia d'età",
            ["Seleziona...", "Fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", 
             "51-60 anni", "61-70 anni", "Più di 70 anni"]
        )

    st.write("---")
    st.subheader("Questionario")

    # Definizione domande
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

    options_map = {
        "per niente d'accordo": 1,
        "poco d'accordo": 2,
        "né d'accordo né in disaccordo": 3,
        "abbastanza d'accordo": 4,
        "totalmente d'accordo": 5
    }
    options_list = list(options_map.keys())
    
    with st.form("ses_questionnaire"):
        scores = []
        answers_log = {}
        
        for q in questions:
            st.markdown(f"**{q['text']}**")
            response = st.radio(
                f"Risp {q['id']}", 
                options_list, 
                index=2, 
                key=f"q_{q['id']}", 
                label_visibility="collapsed"
            )
            
            raw_score = options_map[response]
            final_score = 6 - raw_score if q['reverse'] else raw_score
            scores.append(final_score)
            answers_log[f"Q{q['id']}"] = final_score
            st.markdown("---")
        
        submitted = st.form_submit_button("Calcola Risultati e Salva")

    if submitted:
        if genere == "Seleziona..." or eta == "Seleziona...":
            st.error("Per favore, compila i campi Genere ed Età prima di calcolare i risultati.")
        else:
            average_score = sum(scores) / len(scores)
            
            # SALVATAGGIO DATI
            if HAS_GSHEETS:
                try:
                    record = {
                        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Genere": genere,
                        "Età": eta,
                        "Punteggio_Medio": average_score,
                        **answers_log
                    }
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    existing_data = conn.read(ttl=0)
                    updated_data = pd.concat([existing_data, pd.DataFrame([record])], ignore_index=True)
                    conn.update(data=updated_data)
                    st.toast("Dati salvati correttamente nel Drive!", icon="✅")
                except Exception as e:
                    st.error(f"Errore nel salvataggio remoto: {e}. Controlla i Secrets.")
            else:
                st.info("Salvataggio online non disponibile (libreria mancante).")

            # OUTPUT RISULTATI
            st.header("Il tuo Profilo di Self-Empowerment")
            
            if average_score <= 3:
                result_level = "BASSO"
                result_color = "red"
                desc = "Percezione limitata delle possibilità di influenza. Focus prevalente sui vincoli."
            elif average_score <= 4:
                result_level = "MEDIO"
                result_color = "orange"
                desc = "Livello intermedio. Equilibrio tra percezione di vincoli e risorse."
            else:
                result_level = "ALTO"
                result_color = "green"
                desc = "Ottima percezione delle risorse e forte senso di agenzia (agency)."

            st.markdown(f"### Livello: :{result_color}[{result_level}]")
            st.markdown(f"**Punteggio:** {average_score:.2f} / 5.00")
            st.info(desc)

            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = average_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [1, 5]},
                    'bar': {'color': result_color},
                    'steps': [
                        {'range': [1, 3], 'color': '#ffcccc'},
                        {'range': [3, 4], 'color': '#ffedcc'},
                        {'range': [4, 5], 'color': '#ccffcc'}
                    ],
                    'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': average_score}
                }
            ))
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
