import streamlit as st
import yaml

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
    return yaml.dump(table, default_flow_style=False)

# Streamlit UI components
st.title("Flashcard Processor")

# Input text fields
additional_text = st.text_input("Additional text for 'Lernkarteien'")
input_text = st.text_area("Enter Flashcards (separate cards with blank lines)")

if st.button("Process Flashcards"):
    if not input_text.strip():
        st.error("Please enter some flashcards before processing.")
    else:
        flashcards = input_text.split('\n\n')
        
        # Method 1
        tables1 = create_table_method1(flashcards, additional_text)
        output_text1 = "\n\n".join(format_table_for_output(table) for table in tables1)
        st.subheader("Method 1 Output:")
        st.code(output_text1, language="yaml")
        st.download_button("Copy Method 1 Output", data=output_text1, file_name="method1_output.yaml")
        
        # Method 2
        flashcard_batches2 = create_batches(flashcards)
        tables2 = [create_table_method2(batch, additional_text) for batch in flashcard_batches2]
        output_text2 = "\n\n".join(format_table_for_output(table) for table in tables2)
        st.subheader("Method 2 Output:")
        st.code(output_text2, language="yaml")
        st.download_button("Copy Method 2 Output", data=output_text2, file_name="method2_output.yaml")
        
        # Method 📌
        pin_content = extract_emoji_content(flashcards, '📌')
        st.subheader("📌 Content:")
        st.code(pin_content, language="yaml")
        st.download_button("Copy 📌 Content", data=pin_content, file_name="pin_content.yaml")
        
        # Method 🔍
        magnifier_content = extract_emoji_content(flashcards, '🔍')
        st.subheader("🔍 Content:")
        st.code(magnifier_content, language="yaml")
        st.download_button("Copy 🔍 Content", data=magnifier_content, file_name="magnifier_content.yaml")
