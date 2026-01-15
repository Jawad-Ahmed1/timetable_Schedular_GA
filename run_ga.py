# run_ga.py
from src.ga_timetable import GeneticAlgorithmTimetable
import pandas as pd

def display_section_subjects(df_tt):
    """Display subjects for each section"""
    print(f"\n{'='*100}")
    print(f"📚 SUBJECTS BY SECTION")
    print(f"{'='*100}\n")
    
    sections = sorted(df_tt['Class'].unique())
    
    for section in sections:
        section_tt = df_tt[df_tt['Class'] == section]
        subjects = section_tt[['Subject', 'Code', 'Type']].drop_duplicates().sort_values(['Subject'])
        
        print(f"\n┌─ {section} ─┐")
        print("├──────────────────────┬──────────┬──────────┐")
        print("│ Subject              │ Code     │ Type     │")
        print("├──────────────────────┼──────────┼──────────┤")
        
        for _, row in subjects.iterrows():
            subject = str(row['Subject'])[:22].ljust(22)
            code = str(row['Code'])[:8].ljust(8)
            type_label = str(row['Type'])[:8].ljust(8)
            
            print(f"│ {subject} │ {code} │ {type_label} │")
        
        print("└──────────────────────┴──────────┴──────────┘")

def display_section_timetable(df_tt, section):
    """Display timetable for a specific section"""
    section_tt = df_tt[df_tt['Class'] == section]
    if len(section_tt) == 0:
        print(f"❌ No timetable found for section: {section}")
        return
    
    print(f"\n{'='*80}")
    print(f"📚 TIMETABLE FOR SECTION: {section}")
    print(f"{'='*80}\n")
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    for day in days_order:
        day_tt = section_tt[section_tt['Day'] == day].sort_values(['Start Time'])
        if len(day_tt) > 0:
            print(f"\n┌─ {day.upper()} ─┐")
            print("├─────────────┬──────────────┬──────────────┬─────────────┬──────────┐")
            print("│ Time Slot   │ Subject      │ Faculty      │ Room        │ Type     │")
            print("├─────────────┼──────────────┼──────────────┼─────────────┼──────────┤")
            
            for _, row in day_tt.iterrows():
                time_slot = row['Time Slot'][:13].ljust(13)
                subject = str(row['Subject'])[:14].ljust(14)
                faculty = str(row['Faculty'])[:14].ljust(14)
                room = str(row['Room'])[:13].ljust(13)
                type_label = str(row['Type'])[:8].ljust(8)
                
                print(f"│ {time_slot} │ {subject} │ {faculty} │ {room} │ {type_label} │")
            
            print("└─────────────┴──────────────┴──────────────┴─────────────┴──────────┘")
        else:
            print(f"\n┌─ {day.upper()} ─┐")
            print("│ No classes scheduled")
            print("└─────────────────────────┘")

def display_all_days_timetable(df_tt):
    """Display complete timetable organized by day"""
    print(f"\n{'='*100}")
    print(f"📊 COMPLETE TIMETABLE BY DAY (All Classes)")
    print(f"{'='*100}\n")
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in days_order:
        day_tt = df_tt[df_tt['Day'] == day].sort_values(['Start Time'])
        if len(day_tt) > 0:
            print(f"\n┌─ {day.upper()} ─┐")
            print("├─────────────┬──────────┬──────────────┬──────────────┬─────────────┬──────────┐")
            print("│ Time Slot   │ Class    │ Subject      │ Faculty      │ Room        │ Type     │")
            print("├─────────────┼──────────┼──────────────┼──────────────┼─────────────┼──────────┤")
            
            for _, row in day_tt.iterrows():
                time_slot = row['Time Slot'][:13].ljust(13)
                cls = str(row['Class'])[:8].ljust(8)
                subject = str(row['Subject'])[:14].ljust(14)
                faculty = str(row['Faculty'])[:14].ljust(14)
                room = str(row['Room'])[:13].ljust(13)
                type_label = str(row['Type'])[:8].ljust(8)
                
                print(f"│ {time_slot} │ {cls} │ {subject} │ {faculty} │ {room} │ {type_label} │")
            
            print("└─────────────┴──────────┴──────────────┴──────────────┴─────────────┴──────────┘")

def main():
    print("INTELLIGENT TIMETABLE GA SYSTEM\n")
    ga = GeneticAlgorithmTimetable(csv_file="timetable_data.csv")
    timetable, fitness = ga.run(generations=50, population_size=20)
    
    if timetable:
        print(f"✅ Timetable generated! Fitness: {fitness}\n")
        df_tt = pd.DataFrame(timetable)
        df_tt.to_csv("final_timetable.csv", index=False)
        print("📄 Timetable saved as final_timetable.csv\n")
        
        # Display complete timetable by day
        display_all_days_timetable(df_tt)
        
        # Display subjects by section
        display_section_subjects(df_tt)
        
        # Display timetable for specific sections
        print("\n" + "="*80)
        print("📋 TIMETABLE BY SECTION")
        print("="*80)
        
        sections = sorted(df_tt['Class'].unique())
        for section in sections:
            display_section_timetable(df_tt, section)
    else:
        print("❌ Failed to generate timetable!")

if __name__ == "__main__":
    main()

