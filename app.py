import streamlit as st

def create_table_method1(flashcards, additional_text):
    headers = [card.split('\n')[0] for card in flashcards]
    points = len(flashcards) * 0.5  # 0.5 points per flashcard
    
    tables = []
    
    for emoji_index, emoji in enumerate(['📌', '🔍', '👉']):
        table = [
            ["Typ", "Drag&drop"],
            ["Title", f"Lernkarteien {additional_text}"],
            ["Question", "Ordnen Sie die Definitionen und Beispielen den richtigen Begriffen zu."],
            ["Points", str(points)],
            [""] + headers
        ]
        
        for card in flashcards:
            lines = card.split('\n')
            for line in lines[1:]:
                if line.startswith(emoji):
                    content = line.replace(emoji, "").strip().replace("ß", "ss")
                    row = [content] + ["-0.25" for _ in headers]
                    row[headers.index(lines[0]) + 1] = "0.5"
                    table.append(row)
                    break
        
        table.append([""] * (len(headers) + 1))
        tables.append(table)
    
    return tables

def create_batches(flashcards, batch_size=4):
    batches = [flashcards[i:i + batch_size] for i in range(0, len(flashcards), batch_size)]
    if len(batches[-1]) < batch_size and len(batches) > 1:
        last_batch_needed = batch_size - len(batches[-1])
        for i in range(last_batch_needed):
            batches[-1].append(batches[-2][i % len(batches[-2])])
    return batches

def create_table_method2(flashcards, additional_text):
    headers = [card.split('\n')[0] for card in flashcards]
    points = len(flashcards) * 1.5  # 1.5 points per flashcard (0.5 for each of the three lines)
    
    table = [
        ["Typ", "Drag&drop"],
        ["Title", "Lernkarteien " + additional_text],
        ["Question", "Ordnen Sie die Definitionen und Beispielen den richtigen Begriffen zu."],
        ["Points", str(points)],
        [""] + headers
    ]
    
    for card in flashcards:
        lines = card.split('\n')
        title = lines[0]
        for line in lines[1:]:
            row = [line.replace("📌", "").replace("🔍", "").replace("👉", "").strip()]
            for header in headers:
                row.append("0.5" if header == title else "-0.25")
            table.append(row)
    
    return table

def extract_emoji_content(flashcards, emoji):
    content = []
    for card in flashcards:
        lines = card.split('\n')
        title = lines[0]
        for line in lines[1:]:
            if line.startswith(emoji):
                content.append(f"{title}\n{line}")
                break
    return '\n\n'.join(content)

def format_table_for_output(table):
    # Create a plain tabular format as a string with tab-separated values
    return "\n".join("\t".join(str(cell) for cell in row) for row in table)

# Streamlit UI components
st.title("Flashcard Processor")

# Input text fields
additional_text = st.text_input("OLAT-Fragen werden als 'Lernkarteien' betitelt. Hier kann man einen zusätzlichen Begriff für eine thematische Betitelung")
input_text = st.text_area("Füge die vom Bot erstellte Lernkarteien hier ein.")

if st.button("Process Flashcards"):
    if not input_text.strip():
        st.error("Please enter some flashcards before processing.")
    else:
        flashcards = input_text.split('\n\n')
        
      
        # Method 📌
        pin_content = extract_emoji_content(flashcards, '📌')
        st.subheader("Neue Lernkarteien zum Importieren nur mit 📌-Zeilen:")
        st.text_area("Inhalte kopieren und als Lernkarteien auf Quizlet importieren", pin_content)
        
        # Method 🔍
        magnifier_content = extract_emoji_content(flashcards, '🔍')
        st.subheader("Neue Lernkarteien zum Importieren nur mit 🔎-Zeilen:")
        st.text_area("Inhalte kopieren und als Lernkarteien auf Quizlet importieren", magnifier_content)

        # Method 1
        tables1 = create_table_method1(flashcards, additional_text)
        output_text1 = "\n\n".join(format_table_for_output(table) for table in tables1)
        
        # Updated text with proper line breaks
        info_text = """
        Wandelt die alle Lernkarteien in 3 OLAT-Drag&Drop-Fragen um. 
        Frage 1 = 📌-Rückseite zur Vorderseite zuordnen. 
        Frage 2 = 🔎-Rückseite zur Vorderseite zuordnen. 
        Frage 3 = 👉-Rückseite zur Vorderseite zuordnen.
        
        Inhalte kopieren und in einem OLAT-Test importieren.
        """
        
        st.subheader("OLAT-Import 1:")
        st.text_area(info_text, output_text1)
        
        # Method 2
        flashcard_batches2 = create_batches(flashcards)
        tables2 = [create_table_method2(batch, additional_text) for batch in flashcard_batches2]
        output_text2 = "\n\n".join(format_table_for_output(table) for table in tables2)
        
        # Updated text with proper line breaks and special characters
        info_text2 = """
        Wandelt Gruppen von 4 Lernkarteien OLAT-Drag&Drop-Fragen um.
        Jede Frage lässt die 📌-🔎-👉-Rückseiten von 4 Lernkarteien den Vorderseite zuordnen.
        
        Inhalte kopieren und in einem OLAT-Test importieren.
        """
        
        st.subheader("OLAT-Import 2:")
        st.text_area(info_text2, output_text2)
