import random
import pandas as pd
from .utils import generate_time_slots, generate_classrooms, load_data

class GeneticAlgorithmTimetable:
    def __init__(self, csv_file="timetable_data.csv"):
        self.df = load_data(csv_file)
        self.time_slots = generate_time_slots()
        self.classrooms = generate_classrooms()
    
    # Convert hours to lecture blocks
    def get_lecture_blocks(self, hours):
        blocks = []
        if hours <= 0:
            return blocks
        while hours > 0:
            if hours >= 3:
                blocks.append(3)
                hours -= 3
            elif hours >= 2:
                blocks.append(2)
                hours -= 2
            else:
                blocks.append(1)
                hours -= 1
        return blocks
    
    # Find consecutive slots
    def find_consecutive_slots(self, day, duration, used_slots):
        available_slots = []
        time_mapping = {
            '08:00-09:00': 1,
            '09:00-10:00': 2,
            '10:00-11:00': 3,
            '11:00-12:00': 4,
            '12:00-13:00': 5,
            '13:00-14:00': 6,
            '14:00-15:00': 7,
            '15:00-16:00': 8
        }
        reverse_mapping = {v: k for k, v in time_mapping.items()}
        for start_slot in range(1, 9 - duration + 1):
            consecutive = True
            slots_needed = []
            for i in range(duration):
                slot_num = start_slot + i
                time_slot = reverse_mapping[slot_num]
                key = (day, time_slot)
                if key in used_slots:
                    consecutive = False
                    break
                slots_needed.append(time_slot)
            if consecutive:
                available_slots.append({'start': reverse_mapping[start_slot],
                                        'slots': slots_needed,
                                        'duration': duration})
        return available_slots
    
    # Create one timetable with proper lecture/lab distribution
    def create_individual(self):
        timetable = []
        used_slots = set()
        used_faculty_slots = set()
        used_class_slots = set()
        daily_class_hours = {}
        daily_faculty_hours = {}
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        
        for _, row in self.df.iterrows():
            hours = int(row['Hours']) if pd.notna(row['Hours']) else 0
            if hours <= 0:
                continue
            
            class_name = str(row['Class'])
            subject = str(row['Subject'])
            subject_type = str(row['Type']) if 'Type' in row else 'Theory'
            
            # Determine lecture and lab distribution based on credit hours
            lectures = []
            labs = []
            
            if hours == 3:
                # 3 credit hours: 2 theory lectures (1.5 each, rounded to 1-2 hours) + 1 lab (1 hour)
                lectures = [2, 1]  # 2 lectures: 2 hours and 1 hour
                labs = [1]  # 1 lab: 1 hour
            elif hours == 2:
                # 2 credit hours: 1 theory lecture (2 hours)
                lectures = [2]
                labs = []
            elif hours == 1:
                # 1 credit hour: 1 lecture (1 hour)
                lectures = [1]
                labs = []
            else:
                # For other hours, distribute appropriately
                while hours > 0:
                    if hours >= 3:
                        lectures.append(2)
                        hours -= 2
                        if hours >= 1:
                            labs.append(1)
                            hours -= 1
                    elif hours >= 2:
                        lectures.append(2)
                        hours -= 2
                    else:
                        lectures.append(1)
                        hours -= 1
            
            # Schedule all lectures on different days
            used_days_for_subject = set()
            
            for lecture_duration in lectures:
                placed = False
                max_attempts = 100
                available_days = [d for d in days if d not in used_days_for_subject]
                
                for attempt in range(max_attempts):
                    if not available_days:
                        available_days = [d for d in days if d not in used_days_for_subject]
                    
                    day = random.choice(available_days)
                    available_slots = self.find_consecutive_slots(day, lecture_duration, used_slots)
                    
                    if not available_slots:
                        available_days.remove(day) if day in available_days else None
                        continue
                    
                    slot_info = random.choice(available_slots)
                    start_time = slot_info['start']
                    start_hour = int(start_time.split(':')[0])
                    end_hour = start_hour + lecture_duration
                    time_range = f"{start_hour:02d}:00-{end_hour:02d}:00"
                    
                    # Choose theory room
                    available_rooms = [r for r in self.classrooms if 'Lab' not in r]
                    if not available_rooms:
                        continue
                    room = random.choice(available_rooms)
                    
                    # Faculty list
                    faculties = [f.strip() for f in str(row['Faculty']).split(';')]
                    
                    # Check conflicts
                    conflict = False
                    for slot in slot_info['slots']:
                        if (day, slot, room) in used_slots:
                            conflict = True
                            break
                        for faculty in faculties:
                            if (day, slot, faculty) in used_faculty_slots:
                                conflict = True
                                break
                        if (day, slot, class_name) in used_class_slots:
                            conflict = True
                            break
                        if conflict:
                            break
                    if conflict:
                        continue
                    
                    # Check daily hour limits (increased from 4 to 6 hours)
                    if daily_class_hours.get((class_name, day),0) + lecture_duration > 6:
                        continue
                    
                    faculty_conflict = False
                    for faculty in faculties:
                        if daily_faculty_hours.get((faculty, day),0) + lecture_duration > 7:  # Increased from 5 to 7
                            faculty_conflict = True
                            break
                    if faculty_conflict:
                        continue
                    
                    # Place the lecture
                    entry = {
                        'Class': class_name,
                        'Subject': subject,
                        'Faculty': str(row['Faculty']),
                        'Code': str(row['Code']) if 'Code' in row else '',
                        'Type': 'Theory',
                        'Day': day,
                        'Start Time': f"{start_hour:02d}:00",
                        'End Time': f"{end_hour:02d}:00",
                        'Duration': f"{lecture_duration} hour{'s' if lecture_duration>1 else ''}",
                        'Time Slot': time_range,
                        'Room': room,
                        'Total Hours': hours
                    }
                    timetable.append(entry)
                    for slot in slot_info['slots']:
                        used_slots.add((day, slot, room))
                        for faculty in faculties:
                            used_faculty_slots.add((day, slot, faculty))
                        used_class_slots.add((day, slot, class_name))
                    daily_class_hours[(class_name, day)] = daily_class_hours.get((class_name, day),0) + lecture_duration
                    for faculty in faculties:
                        daily_faculty_hours[(faculty, day)] = daily_faculty_hours.get((faculty, day),0) + lecture_duration
                    
                    used_days_for_subject.add(day)
                    placed = True
                    break
            
            # Schedule all labs on different days
            for lab_duration in labs:
                placed = False
                max_attempts = 100
                available_days = [d for d in days if d not in used_days_for_subject]
                
                for attempt in range(max_attempts):
                    if not available_days:
                        available_days = [d for d in days if d not in used_days_for_subject]
                    
                    day = random.choice(available_days)
                    available_slots = self.find_consecutive_slots(day, lab_duration, used_slots)
                    
                    if not available_slots:
                        available_days.remove(day) if day in available_days else None
                        continue
                    
                    slot_info = random.choice(available_slots)
                    start_time = slot_info['start']
                    start_hour = int(start_time.split(':')[0])
                    end_hour = start_hour + lab_duration
                    time_range = f"{start_hour:02d}:00-{end_hour:02d}:00"
                    
                    # Choose lab room
                    available_rooms = [r for r in self.classrooms if 'Lab' in r]
                    if not available_rooms:
                        continue
                    room = random.choice(available_rooms)
                    
                    # Faculty list
                    faculties = [f.strip() for f in str(row['Faculty']).split(';')]
                    
                    # Check conflicts
                    conflict = False
                    for slot in slot_info['slots']:
                        if (day, slot, room) in used_slots:
                            conflict = True
                            break
                        for faculty in faculties:
                            if (day, slot, faculty) in used_faculty_slots:
                                conflict = True
                                break
                        if (day, slot, class_name) in used_class_slots:
                            conflict = True
                            break
                        if conflict:
                            break
                    if conflict:
                        continue
                    
                    # Check daily hour limits
                    if daily_class_hours.get((class_name, day),0) + lab_duration > 6:
                        continue
                    
                    faculty_conflict = False
                    for faculty in faculties:
                        if daily_faculty_hours.get((faculty, day),0) + lab_duration > 7:
                            faculty_conflict = True
                            break
                    if faculty_conflict:
                        continue
                    
                    # Place the lab
                    entry = {
                        'Class': class_name,
                        'Subject': subject,
                        'Faculty': str(row['Faculty']),
                        'Code': str(row['Code']) if 'Code' in row else '',
                        'Type': 'Lab',
                        'Day': day,
                        'Start Time': f"{start_hour:02d}:00",
                        'End Time': f"{end_hour:02d}:00",
                        'Duration': f"{lab_duration} hour{'s' if lab_duration>1 else ''}",
                        'Time Slot': time_range,
                        'Room': room,
                        'Total Hours': hours
                    }
                    timetable.append(entry)
                    for slot in slot_info['slots']:
                        used_slots.add((day, slot, room))
                        for faculty in faculties:
                            used_faculty_slots.add((day, slot, faculty))
                        used_class_slots.add((day, slot, class_name))
                    daily_class_hours[(class_name, day)] = daily_class_hours.get((class_name, day),0) + lab_duration
                    for faculty in faculties:
                        daily_faculty_hours[(faculty, day)] = daily_faculty_hours.get((faculty, day),0) + lab_duration
                    
                    used_days_for_subject.add(day)
                    placed = True
                    break
        
        return timetable

    def calculate_fitness(self, timetable):
        if not timetable:
            return 0
        
        # Count how many classes were actually scheduled
        scheduled_count = len(timetable)
        total_expected = len(self.df)  # Total classes that should be scheduled
        
        # Penalty for unscheduled classes (most important!)
        if total_expected > 0:
            scheduling_penalty = (total_expected - scheduled_count) * 50  # Heavy penalty
        else:
            scheduling_penalty = 0
        
        # Check for conflicts
        conflict_penalty = 0
        room_slots, faculty_slots, class_slots = {}, {}, {}
        
        for entry in timetable:
            key = (entry['Day'], entry['Time Slot'], entry['Room'])
            if key in room_slots:
                conflict_penalty += 100
            room_slots[key] = entry
            
            for faculty in str(entry['Faculty']).split(';'):
                fkey = (entry['Day'], entry['Time Slot'], faculty.strip())
                if fkey in faculty_slots:
                    conflict_penalty += 75
                faculty_slots[fkey] = entry
            
            ckey = (entry['Day'], entry['Time Slot'], entry['Class'])
            if ckey in class_slots:
                conflict_penalty += 80
            class_slots[ckey] = entry
        
        total_penalty = scheduling_penalty + conflict_penalty
        max_fitness = 1000
        fitness = max(1, max_fitness - total_penalty)
        
        # Normalize to percentage
        normalized_fitness = (fitness / max_fitness) * 100
        
        return round(normalized_fitness, 2)
    
    # CROSSOVER: Breed two good timetables
    def crossover(self, parent1, parent2):
        """Combine two timetables to create offspring"""
        if not parent1 or not parent2:
            return self.create_individual()
        
        # Use multiple crossover strategies for better diversity
        strategy = random.choice(['single_point', 'two_point', 'uniform'])
        
        if strategy == 'single_point':
            # Take first half from parent1, second half from parent2
            split_point = len(parent1) // 2
            offspring = parent1[:split_point] + parent2[split_point:]
        
        elif strategy == 'two_point':
            # Two-point crossover
            split1 = len(parent1) // 3
            split2 = (2 * len(parent1)) // 3
            offspring = parent1[:split1] + parent2[split1:split2] + parent1[split2:]
        
        else:  # uniform
            # Randomly pick from each parent
            offspring = []
            for i in range(len(parent1)):
                offspring.append(random.choice([parent1[i], parent2[i]]))
        
        return offspring
    
    # MUTATION: Randomly modify a timetable
    def mutate(self, timetable):
        """Randomly change some classes in the timetable"""
        if not timetable or len(timetable) == 0:
            return timetable
        
        mutated = [entry.copy() for entry in timetable]
        mutation_rate = 0.3  # 30% chance to mutate (increased from 20%)
        
        for entry in mutated:
            if random.random() < mutation_rate:
                mutation_type = random.choice(['day', 'time', 'room', 'swap'])
                
                if mutation_type == 'day':
                    # Randomly change day
                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                    entry['Day'] = random.choice(days)
                
                elif mutation_type == 'time':
                    # Randomly change time slot
                    entry['Time Slot'] = random.choice(self.time_slots)
                
                elif mutation_type == 'room':
                    # Randomly change room (theory or lab based on type)
                    if entry['Type'] == 'Lab':
                        available_rooms = [r for r in self.classrooms if 'Lab' in r]
                    else:
                        available_rooms = [r for r in self.classrooms if 'Lab' not in r]
                    
                    if available_rooms:
                        entry['Room'] = random.choice(available_rooms)
                
                elif mutation_type == 'swap' and len(mutated) > 1:
                    # Swap with another random entry
                    other_idx = random.randint(0, len(mutated) - 1)
                    mutated[entry.index if hasattr(entry, 'index') else mutated.index(entry)], mutated[other_idx] = mutated[other_idx], entry
                
                # Update start and end times
                if mutation_type in ['time', 'day', 'swap']:
                    start_hour = int(entry['Time Slot'].split(':')[0])
                    duration = int(entry['Duration'].split()[0])
                    end_hour = start_hour + duration
                    entry['Start Time'] = f"{start_hour:02d}:00"
                    entry['End Time'] = f"{end_hour:02d}:00"
        
        return mutated
    
    # SELECTION: Pick best individuals for reproduction
    def selection(self, population, fitness_scores, num_parents=2):
        """Select best parents based on fitness"""
        # Sort by fitness (descending)
        sorted_indices = sorted(range(len(fitness_scores)), 
                               key=lambda i: fitness_scores[i], 
                               reverse=True)
        
        # Return top parents
        parents = [population[i] for i in sorted_indices[:num_parents]]
        return parents
    
    def run(self, generations=50, population_size=20):
        """Run true Genetic Algorithm with selection, crossover, and mutation"""
        population = [self.create_individual() for _ in range(population_size)]
        best_individual = None
        best_fitness = 0
        fitness_history = []
        
        for gen in range(generations):
            # Calculate fitness for all individuals
            fitness_scores = [self.calculate_fitness(individual) for individual in population]
            
            # Track best in this generation
            current_best_idx = fitness_scores.index(max(fitness_scores))
            current_best_fitness = fitness_scores[current_best_idx]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = population[current_best_idx]
            
            fitness_history.append(best_fitness)
            
            # SELECTION: Select best parents
            parents = self.selection(population, fitness_scores, num_parents=4)
            
            # Create new generation
            new_population = [best_individual]  # Keep best (elitism)
            
            while len(new_population) < population_size:
                # CROSSOVER: Breed parents
                parent1, parent2 = random.sample(parents, 2)
                offspring = self.crossover(parent1, parent2)
                
                # MUTATION: Mutate offspring
                offspring = self.mutate(offspring)
                
                new_population.append(offspring)
            
            population = new_population
        
        return best_individual, best_fitness
