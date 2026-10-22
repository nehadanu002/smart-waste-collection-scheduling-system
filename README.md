# Smart Waste Collection Scheduling System

A web-based application that helps improve waste collection by prioritizing waste bins according to their fill levels and generating an efficient collection route.

## 📌 Project Overview

The Smart Waste Collection Scheduling System is developed to make waste collection more organized and efficient. It allows users to view waste-bin information, prioritize bins that need collection, and generate a suggested route for collection vehicles.

The project demonstrates the use of **Data Structures and Algorithms (DAA)** in a practical waste-management scenario.

## 🎯 Objectives

- Monitor and manage waste-bin fill levels.
- Prioritize bins that require collection.
- Generate a suggested route for waste collection.
- Reduce unnecessary travel and improve collection planning.
- Demonstrate the practical application of greedy algorithms and route optimization.

## ✨ Features

- **Dashboard:** View waste-bin information and collection status.
- **Bin Management:** Add or update bin details.
- **Priority Scheduling:** Rank bins based on fill level using a greedy approach.
- **Route Planning:** Suggest a collection route using the Nearest Neighbour heuristic.
- **Collection Tracking:** Mark scheduled collections as completed.
- **Database Integration:** Store application data using SQLite during local development.

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python with Flask
- **Database:** SQLite (local development)
- **Algorithms:** Greedy scheduling and Nearest Neighbour route heuristic
- **Tools:** Visual Studio Code, Git, GitHub

## 🧠 Algorithms Used

### 1. Greedy Priority Scheduling

Waste bins are sorted according to their fill levels so that fuller bins receive higher priority. In the implementation, bins with a fill level of at least 35% are considered for scheduling.

**Time Complexity:** \(O(n \log n)\) for sorting \(n\) bins.

### 2. Nearest Neighbour Route Planning

The algorithm repeatedly selects the nearest unvisited collection point from the current location. It provides a practical route suggestion, but it does not guarantee the globally shortest route.

**Time Complexity:** Typically \(O(n^2)\) for a straightforward implementation with \(n\) collection points.

## 📂 Project Structure

```text
smart_waste_collection_system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── base.html
    ├── index.html
    ├── schedule.html
    └── route.html
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version
- Git
- A code editor such as Visual Studio Code

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/nehadanu002/smart-waste-collection-scheduling-system.git
   ```

2. Move into the project directory:

   ```bash
   cd smart-waste-collection-scheduling-system
   ```

3. Create and activate a virtual environment:

   **Windows PowerShell**
   
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open the local URL displayed in the terminal, usually:

   `http://127.0.0.1:5000`

## 🚀 Future Scope

- Integrate GPS-based location tracking.
- Use real-time fill-level sensors.
- Connect the application to a persistent cloud database.
- Improve route optimization for larger numbers of bins.
- Add user authentication and administrative controls.
- Deploy the application online for remote access.

## 🎓 Academic Purpose

This project demonstrates the practical application of algorithm design, scheduling, route planning, database management, and web development for a real-world waste-management problem.

## 👩‍💻 Author

**Neha Danu**

MCA (Data Science)

## 📄 License

This project is developed for educational and academic purposes.
