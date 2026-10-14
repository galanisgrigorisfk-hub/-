import json
import os
import re
import unicodedata

ARCHEIO = "programma_mathimaton.json"

def afairesi_tonon(keimeno):
    nfkd_form = unicodedata.normalize('NFKD', keimeno)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def format_time(ora):
    ora = ora.strip()
    if ora.isdigit():
        num = int(ora)
        if 0 <= num <= 23:
            return f"{num:02d}:00"
    return ora

def is_valid_time(ora):
    pattern = r"^\d{1,2}:\d{2}$"
    return bool(re.match(pattern, ora))

def fortose_programma():
    if os.path.exists(ARCHEIO):
        with open(ARCHEIO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "δευτερα": [], "τριτη": [], "τεταρτη": [], 
        "πεμπτη": [], "παρασκευη": [], "σαββατο": [], "κυριακη": []
    }

def apothikefse_programma(programma):
    with open(ARCHEIO, "w", encoding="utf-8") as f:
        json.dump(programma, f, ensure_ascii=False, indent=4)

def main():
    programma = fortose_programma()
    meres = ["δευτερα", "τριτη", "τεταρτη", "πεμπτη", "παρασκευη", "σαββατο", "κυριακη"]

    while True:
        print("\n=== ΠΡΟΓΡΑΜΜΑ ΜΑΘΗΜΑΤΩΝ ===")
        print("1. Προβολή προγράμματος ημέρας")
        print("2. Μαζική καταχώριση/Αλλαγή προγράμματος (όλη η εβδομάδα)")
        print("3. Προσθήκη μαθήματος σε συγκεκριμένη μέρα")
        print("4. Επεξεργασία μαθήματος (Ώρα/Όνομα/Σχόλιο)")
        print("5. Διαγραφή μαθήματος από μέρα")
        print("6. Αναζήτηση μαθήματος στην εβδομάδα")
        print("7. Έξοδος")
        
        epilogi = input("Επιλέξτε ενέργεια (1-7): ").strip()
        
        if epilogi == "1":
            input_imera = input("Ποια μέρα θέλεις να ελέγξεις; ")
            imera = afairesi_tonon(input_imera).strip().lower()
            
            if imera in programma:
                mathimata = programma[imera]
                print(f"\n--- Πρόγραμμα για {input_imera.capitalize()} ---")
                if mathimata:
                    for m in mathimata:
                        print(f" - {m}")
                else:
                    print(" Δεν υπάρχουν μαθήματα καταχωρημένα για αυτή τη μέρα.")
            else:
                print("\n⚠️ Άγνωστη μέρα.")
                
        elif epilogi == "2":
            print("\n--- Μαζική Καταχώριση Εβδομάδας ---")
            print("Μπορείς να γράφεις π.χ. '9' (γίνεται 09:00) ή '09:30'. Πατήστε Enter στην Ώρα Έναρξης για τέλος μέρας.")
            
            for m in meres:
                print(f"\nΜέρα: {m.capitalize()}")
                nea_mathimata = []
                
                while True:
                    enarxi_input = input(f"Ώρα Έναρξης (π.χ. 9 ή 09:00, ή Enter για επόμενη μέρα): ").strip()
                    if enarxi_input == "":
                        break
                    
                    enarxi = format_time(enarxi_input)
                    while not is_valid_time(enarxi):
                        print("⚠️ Λάθος μορφή ώρας! Χρησιμοποίησε τη μορφή ΩΩ:ΛΛ (π.χ. 9 ή 09:00).")
                        enarxi_input = input(f"Ώρα Έναρξης: ").strip()
                        enarxi = format_time(enarxi_input)
                    
                    lixi_input = input(f"Ώρα Λήξης (π.χ. 10 ή 10:30, ή Enter για χωρίς λήξη): ").strip()
                    lixi = ""
                    if lixi_input:
                        lixi = format_time(lixi_input)
                        while not is_valid_time(lixi):
                            print("⚠️ Λάθος μορφή ώρας λήξης! Δοκίμασε ξανά.")
                            lixi_input = input(f"Ώρα Λήξης: ").strip()
                            lixi = format_time(lixi_input)
                        
                    onoma = input(f"Όνομα μαθήματος: ").strip()
                    while not onoma:
                        print("⚠️ Το όνομα του μαθήματος δεν μπορεί να είναι κενό.")
                        onoma = input(f"Όνομα μαθήματος: ").strip()
                    
                    scholio = input(f"Σχόλιο / Σημείωση (προαιρετικό, π.χ. Αίθουσα 3): ").strip()

                    # Δόμηση τελικού κειμένου
                    tekst = f"{enarxi}"
                    if lixi:
                        tekst += f" - {lixi}"
                    tekst += f" : {onoma}"
                    if scholio:
                        tekst += f" ({scholio})"
                        
                    nea_mathimata.append(tekst)
                
                if nea_mathimata:
                    programma[m] = nea_mathimata
            
            apothikefse_programma(programma)
            print("\n✅ Ολόκληρο το πρόγραμμα της εβδομάδας ενημερώθηκε και αποθηκεύτηκε!")

        elif epilogi == "3":
            input_imera = input("Σε ποια μέρα θέλεις να προσθέσεις μάθημα; ")
            imera = afairesi_tonon(input_imera).strip().lower()
            
            if imera in programma:
                while True:
                    enarxi_input = input("Δώσε ώρα έναρξης (π.χ. 9 ή 09:00): ").strip()
                    enarxi = format_time(enarxi_input)
                    if is_valid_time(enarxi):
                        break
                    print("⚠️ Μη έγκυρη ώρα! Δοκίμασε ξανά.")
                
                lixi = ""
                while True:
                    lixi_input = input("Δώσε ώρα λήξης (π.χ. 10 ή 10:30, ή άστο κενό): ").strip()
                    if lixi_input == "":
                        break
                    lixi = format_time(lixi_input)
                    if is_valid_time(lixi):
                        break
                    print("⚠️ Μη έγκυρη ώρα λήξης! Δοκίμασε ξανά.")
                
                while True:
                    mathima = input("Δώσε το όνομα του μαθήματος: ").strip()
                    if mathima:
                        break
                    print("⚠️ Το όνομα δεν μπορεί να είναι κενό.")
                
                scholio = input("Δώσε σχόλιο / σημείωση (προαιρετικό): ").strip()

                tekst = f"{enarxi}"
                if lixi:
                    tekst += f" - {lixi}"
                tekst += f" : {mathima}"
                if scholio:
                    tekst += f" ({scholio})"
                    
                programma[imera].append(tekst)
                apothikefse_programma(programma)
                print(f"✅ Το μάθημα προστέθηκε επιτυχώς στην {input_imera.capitalize()}!")
            else:
                print("\n⚠️ Άγνωστη μέρα.")

        elif epilogi == "4":
            input_imera = input("Σε ποια μέρα βρίσκεται το μάθημα που θες να επεξεργαστείς; ")
            imera = afairesi_tonon(input_imera).strip().lower()
            
            if imera in programma:
                mathimata = programma[imera]
                if not mathimata:
                    print(f"\n⚠️ Η {input_imera.capitalize()} δεν έχει μαθήματα για επεξεργασία.")
                else:
                    print(f"\n--- Μαθήματα για {input_imera.capitalize()} ---")
                    for i, m in enumerate(mathimata, 1):
                        print(f"{i}. {m}")
                    
                    try:
                        arithmos = int(input("Δώσε τον αριθμό του μαθήματος που θέλεις να επεξεργαστείς: "))
                        if 1 <= arithmos <= len(mathimata):
                            print("\nΔώσε τα νέα στοιχεία (άστο κενό αν θες να κρατήσεις το προηγούμενο):")
                            
                            # Νέα Ώρα Έναρξης
                            enarxi_input = input("Νέα ώρα έναρξης: ").strip()
                            enarxi = format_time(enarxi_input) if enarxi_input else ""
                            while enarxi_input and not is_valid_time(enarxi):
                                print("⚠️ Λάθος μορφή ώρας!")
                                enarxi_input = input("Νέα ώρα έναρξης: ").strip()
                                enarxi = format_time(enarxi_input) if enarxi_input else ""

                            # Νέα Ώρα Λήξης
                            lixi_input = input("Νέα ώρα λήξης: ").strip()
                            lixi = format_time(lixi_input) if lixi_input else ""
                            while lixi_input and not is_valid_time(lixi):
                                print("⚠️ Λάθος μορφή ώρας λήξης!")
                                lixi_input = input("Νέα ώρα λήξης: ").strip()
                                lixi = format_time(lixi_input) if lixi_input else ""

                            # Νέο Όνομα
                            neo_onoma = input("Νέο όνομα μαθήματος: ").strip()

                            # Νέο Σχόλιο
                            neo_scholio = input("Νέο σχόλιο / σημείωση: ").strip()

                            # Ανακατασκευή με βάση το τι έδωσε ο χρήστης (ή κράτημα του παλιού)
                            palio = mathimata[arithmos - 1]
                            
                            # (Απλοποιημένη προσέγγιση: αντικαθιστούμε ολόκληρο το μάθημα με νέα είσοδο)
                            print(f"Προηγούμενο: {palio}")
                            
                            # Αν ο χρήστης δεν έδωσε νέα στοιχεία για κάποιο πεδίο, θα μπορούσαμε να τα κρατήσουμε, 
                            # αλλά για απλότητα στην Python, ας ξαναζητήσουμε τα βασικά ή ας τα αφήσουμε να αντικατασταθούν.
                            # Ας κάνουμε μια έξυπνη ανακατασκευή:
                            
                        else:
                            print("⚠️ Ο αριθμός που έδωσες δεν υπάρχει στη λίστα.")
                    except ValueError:
                        print("⚠️ Παρακαλώ δώσε έναν έγκυρο αριθμό.")
            else:
                print("\n⚠️ Άγνωστη μέρα.")

        elif epilogi == "5":
            input_imera = input("Από ποια μέρα θέλεις να διαγράψεις μάθημα; ")
            imera = afairesi_tonon(input_imera).strip().lower()
            
            if imera in programma:
                mathimata = programma[imera]
                if not mathimata:
                    print(f"\n⚠️ Η {input_imera.capitalize()} δεν έχει μαθήματα για διαγραφή.")
                else:
                    print(f"\n--- Μαθήματα για {input_imera.capitalize()} ---")
                    for i, m in enumerate(mathimata, 1):
                        print(f"{i}. {m}")
                    
                    try:
                        arithmos = int(input("Δώσε τον αριθμό του μαθήματος που θέλεις να διαγράψεις: "))
                        if 1 <= arithmos <= len(mathimata):
                            diagrammeno = mathimata.pop(arithmos - 1)
                            apothikefse_programma(programma)
                            print(f"✅ Το μάθημα '{diagrammeno}' διαγράφηκε επιτυχώς!")
                        else:
                            print("⚠️ Ο αριθμός που έδωσες δεν υπάρχει στη λίστα.")
                    except ValueError:
                        print("⚠️ Παρακαλώ δώσε έναν έγκυρο αριθμό.")
            else:
                print("\n⚠️ Άγνωστη μέρα.")

        elif epilogi == "6":
            query_input = input("Ποιο μάθημα θέλεις να αναζητήσεις; ")
            query = afairesi_tonon(query_input).strip().lower()
            
            vrethike = False
            print(f"\n--- Αποτελέσματα αναζήτησης για '{query_input}' ---")
            
            for imera, mathimata in programma.items():
                for m in mathimata:
                    if query in afairesi_tonon(m).lower():
                        print(f"📌 {imera.capitalize()}: {m}")
                        vrethike = True
                        
            if not vrethike:
                print("⚠️ Δεν βρέθηκε κανένα μάθημα με αυτό το όνομα.")
                
        elif epilogi == "7":
            print("Γεια σας! 👋")
            break
        else:
            print("⚠️ Μη αποδεκτή επιλογή. Παρακαλώ επιλέξτε από 1 έως 7.")

if __name__ == "__main__":
    main()