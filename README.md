# 📚 Intelligent Timetable Scheduling System

A genetic algorithm-based timetable scheduler with an interactive Streamlit web interface.

## Features

✅ **Conflict-Free Scheduling** - No room, faculty, or class conflicts
✅ **Intelligent Distribution** - Lectures and labs spread across different days
✅ **Workload Management** - Respects faculty and class hour limits
✅ **Interactive Dashboard** - View timetables in multiple formats
✅ **Export Options** - Download as CSV or Excel

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use

1. **Open the App** - Run the command above
2. **Configure Settings** (Optional)
   - Adjust Generations (10-100)
   - Adjust Population Size (5-50)
3. **Generate Timetable** - Click the "Generate Timetable" button
4. **View Results**:
   - **📊 Daily Schedule** - See all classes by day
   - **📚 Subjects** - View subjects per section
   - **🏫 By Section** - Select and view specific section schedules
   - **📥 Download** - Export timetable as CSV or Excel

## Project Structure

```
Timetable_System/
├── streamlit_app.py          # Main Streamlit web app
├── run_ga.py                 # Console version (optional)
├── timetable_data.csv        # Course data
├── final_timetable.csv       # Generated timetable output
├── requirements.txt          # Python dependencies
└── src/
    ├── ga_timetable.py       # Genetic Algorithm implementation
    └── utils.py              # Utility functions
```

## Data Format

The `timetable_data.csv` must contain:
- `Class` - Section name (e.g., BSCS-4A)
- `StudentGroup` - Student group
- `Subject` - Subject name
- `Code` - Course code
- `Type` - Theory or Lab
- `Hours` - Credit hours
- `FacultyID` - Faculty identifier
- `Faculty` - Faculty name
- `Program` - Program name (BSCS, SE, etc.)
- `Semester` - Semester number
- `RoomType` - Theory or Lab

## Algorithm Details

### Credit Hour Distribution
- **3 hours**: 2 lectures (2hrs + 1hr) + 1 lab (1hr)
- **2 hours**: 1 lecture (2hrs)
- **1 hour**: 1 lecture (1hr)

### Constraints
- Max 4 hours per class per day
- Max 5 hours per faculty per day
- No overlapping room/faculty/class usage
- Lectures and labs on different days for same subject

### Fitness Function
Penalizes:
- Room conflicts: -100
- Faculty conflicts: -75
- Class conflicts: -80

## Tips

💡 **Better Results**:
- Increase generations for better optimization
- Increase population size for more diversity
- Ensure enough rooms and time slots for all courses

🚀 **Performance**:
- Start with 50 generations and 20 population size
- Adjust up if you have more courses to schedule

## Browser Compatibility

Works best with:
- Chrome/Chromium
- Firefox
- Edge
- Safari

## Troubleshooting

**Issue**: App won't start
- Solution: `pip install --upgrade streamlit`

**Issue**: Missing dependencies
- Solution: `pip install -r requirements.txt --upgrade`

**Issue**: Can't generate timetable
- Solution: Check `timetable_data.csv` format and ensure all required columns exist

---

**Author**: Intelligent Timetable System  
**Version**: 1.0  
**License**: MIT
