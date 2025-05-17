# Ambulance-Allocation-Optimization-Using-Tabu-Search
Optimization algorithm to determine optimal ambulance placement based on real accident data from Aguascalientes (2019).


## Strategic Ambulance Placement with Tabu Search

This project tackles the problem of strategically placing a limited number of ambulances across the state of Aguascalientes, Mexico, using **metaheuristic optimization**. The main goal is to **minimize emergency response times** by maximizing accident coverage with the fewest ambulances possible.

The core of the solution is based on the **Tabu Search algorithm**, which iteratively improves candidate solutions while avoiding cycles using a memory structure (the tabu list).

---

## How to Run

### 1. Install Requirements

```bash
pip install pandas numpy folium branca
```

### 2. Run the Optimization

```bash
python Tabu.py
```
This script will output:

- Number of ambulances
- Covered and uncovered accidents
- Total cost
- Optimal coordinates of the ambulances

### 3. Generate Map

After running the optimization, visualize the result by running:

```bash
python mapa.py
```
This will create an HTML file ej_2019_ambulancias_BAS.html with an interactive map showing accident density and ambulance locations.

---

## How It Works

### Tabu Search Overview

- **Initial Solution**: Randomly selects accident locations to place ambulances.
- **Neighborhoods**: Generates neighboring solutions by relocating one ambulance at a time to a new accident site.
- **Tabu List**: A short-term memory that stores recent solutions to prevent cycling or revisiting them.
- **Objective Function**: Calculates total response cost by:
  - Adding the **minimum distance** from each accident to the nearest ambulance (if within the coverage radius).
  - Applying a **penalty of 1000 units** for every accident outside the coverage radius.
- **Result**: The algorithm searches for a placement configuration that minimizes uncovered accidents and ensures efficient emergency response.

### Key Evaluation Metrics

- **Covered Accidents**: Number of incidents within 4 km of at least one ambulance.
- **Uncovered Accidents**: Incidents beyond the coverage radius.
- **Total Cost**: Sum of travel distances + penalties for uncovered points.
- **Final Locations**: Best ambulance positions found during the iterations.

---

## Sample Outputs


---
