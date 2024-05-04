import sys
import requests
import folium
import polyline
import io
import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QListWidget, QLabel
from PyQt5.QtWidgets import QMessageBox ,QScrollArea, QVBoxLayout, QWidget

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

from scipy.optimize import dual_annealing

from deap import base, creator, tools, algorithms
import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import time


# from scipy.optimize import linear_sum_assignment

def get_osrm_route(start, end, server_url="http://router.project-osrm.org"):
    coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    url = f"{server_url}/route/v1/driving/{coords}?overview=full"  # Ensure full geometry is requested
    response = requests.get(url)
    routes = response.json()
    if routes['code'] == 'Ok':
        route_summary = routes['routes'][0]['legs'][0]
        route_geometry = routes['routes'][0]['geometry']  # Get encoded polyline
        return route_summary['distance'], route_geometry
    else:
        raise Exception("OSRM API error: " + routes['code'])
    
def solve_tsp_nearest_neighbor(dist_matrix):
    n = len(dist_matrix)
    start = 0
    visited = [False] * n
    visited[start] = True
    tour = [start]
    total_cost = 0

    current = start
    while len(tour) < n:
        next_index = np.argmin([dist_matrix[current][i] if not visited[i] else np.inf for i in range(n)])
        visited[next_index] = True
        tour.append(next_index)
        total_cost += dist_matrix[current][next_index]
        current = next_index

    total_cost += dist_matrix[tour[-1]][tour[0]]
    tour.append(tour[0])
    return tour, total_cost

def solve_tsp_random_sampling(dist_matrix, samples=10000):
    n = len(dist_matrix)
    cities = range(n)
    best_route = None
    min_cost = float('inf')

    for _ in range(samples):
        route = np.random.permutation(n)
        cost = sum(dist_matrix[route[i]][route[(i + 1) % n]] for i in range(n))
        if cost < min_cost:
            min_cost = cost
            best_route = route.tolist() + [route[0]]

    return best_route, min_cost

def solve_tsp_genetic_algorithm(dist_matrix):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    n = len(dist_matrix)

    # Attribute generator
    toolbox.register("indices", random.sample, range(n), n)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalTSP(individual):
        return sum(dist_matrix[individual[i]][individual[i-1]] for i in range(n)),

    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalTSP)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 50, halloffame=hof)

    return hof[0], evalTSP(hof[0])[0]

def solve_tsp_ant_colony_optimization(dist_matrix, num_ants=20, num_iterations=100, decay=0.5, alpha=1, beta=5):
    
    n = len(dist_matrix)
    pheromones = np.ones((n, n)) * 0.1
    best_cost = float('inf')
    best_route = None
    
    for _ in range(num_iterations):
        for _ in range(num_ants):
            route = [np.random.randint(0, n)]
            for _ in range(1, n):
                current = route[-1]
                probabilities = np.zeros(n)
                
                for j in range(n):
                    if j not in route:
                        if dist_matrix[current][j] > 0:
                            trail_strength = pheromones[current][j] ** alpha
                            visibility = (1.0 / dist_matrix[current][j]) ** beta
                            probabilities[j] = trail_strength * visibility
                
                # Normalize probabilities
                if np.sum(probabilities) == 0:
                    probabilities = np.ones(n) / n  # Equal probability if no valid move found
                else:
                    probabilities /= np.sum(probabilities)  # Normalize
                
                # Check for NaN values explicitly
                if np.isnan(probabilities).any():
                    probabilities = np.ones(n) / n  # Fallback to equal probabilities if NaNs are detected
                
                next_city = np.random.choice(n, p=probabilities)
                route.append(next_city)
            
            route.append(route[0])  # Close the tour
            cost = sum(dist_matrix[route[i]][route[i+1]] for i in range(n))
            if cost < best_cost:
                best_cost = cost
                best_route = route
            
            # Update pheromones
            pheromones *= decay
            for i in range(n):
                pheromones[route[i]][route[(i + 1) % n]] += 1.0 / cost
    
    return best_route, best_cost

def solve_tsp_greedy(dist_matrix):
    n = len(dist_matrix)
    visited = [False] * n
    tour = [0]  # Start at the first city
    visited[0] = True
    total_cost = 0

    current_city = 0
    while len(tour) < n:
        next_city = None
        min_dist = float('inf')
        for i in range(n):
            if not visited[i] and dist_matrix[current_city][i] < min_dist:
                min_dist = dist_matrix[current_city][i]
                next_city = i
        tour.append(next_city)
        visited[next_city] = True
        total_cost += min_dist
        current_city = next_city

    # Return to the starting city
    total_cost += dist_matrix[current_city][tour[0]]
    tour.append(tour[0])
    return tour, total_cost

# def solve_tsp(dist_matrix):
#     row_ind, col_ind = linear_sum_assignment(dist_matrix)
#     total_cost = dist_matrix[row_ind, col_ind].sum()
#     return col_ind, total_cost


class TSPMapApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Solver for Southern California")
        self.setGeometry(100, 100, 19200, 1080)
        self.initUI()

    #def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # Main horizontal layout


        # Applying a global style to the application that works well with both light and dark themes
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;  # Light grey background
                color: #000000;  # Black text
            }
            QLabel, QComboBox, QListWidget, QPushButton {
                background-color: #ffffff;  # White background for input and labels
                color: #000000;  # Black text
            }
        """)


        # Sidebar for input controls
        sidebar = QVBoxLayout()
        start_city_label = QLabel("Starting City")
        sidebar.addWidget(start_city_label)
        self.start_city_dropdown = QComboBox()
        self.start_city_dropdown.addItems(['Los Angeles', 'San Diego', 'Irvine', 'Santa Ana', 'Long Beach', 'Pasadena', 'Malibu', 'Ventura', 'Riverside', 'Bakersfield', 'Anaheim', 'Santa Barbara'])
        sidebar.addWidget(self.start_city_dropdown)

        self.destination_cities_list = QListWidget()
        destination_label = QLabel("Delivery Locations")
        sidebar.addWidget(destination_label)
        self.destination_cities_list.addItems(['Los Angeles', 'San Diego', 'Irvine', 'Santa Ana', 'Long Beach', 'Pasadena', 'Malibu', 'Ventura', 'Riverside', 'Bakersfield', 'Anaheim', 'Santa Barbara'])
        self.destination_cities_list.setSelectionMode(QListWidget.MultiSelection)
        sidebar.addWidget(self.destination_cities_list)

        # Dropdown for selecting the TSP algorithm
        self.algorithm_selection = QComboBox()
        self.algorithm_selection.addItems(['Greedy', 'Nearest Neighbor', 'Random Sampling', 'Genetic Algorithm', 'Ant Colony Optimization'])
        sidebar.addWidget(self.algorithm_selection)

        self.calculate_button = QPushButton('Calculate Route')
        self.calculate_button.clicked.connect(self.calculate_route)
        sidebar.addWidget(self.calculate_button)

        # Existing setup code...
        self.execute_all_button = QPushButton('Execute All')
        self.execute_all_button.clicked.connect(self.execute_all_algorithms)
        sidebar.addWidget(self.execute_all_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_app)
        sidebar.addWidget(self.refresh_button)

        # Main display area for the map and route label
        map_area = QVBoxLayout()  # Vertical layout to keep map and label aligned
        self.map_view = QWebEngineView()
        map_area.addWidget(self.map_view)

        self.route_label = QLabel("Route will be displayed here.")
        self.route_label.setMaximumHeight(30)  # Set a maximum height to the label
        self.route_label.setStyleSheet("padding: 5px;")  # Optional: Adjust padding and background
        map_area.addWidget(self.route_label)

        # Setup for matplotlib chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        map_area.addWidget(self.canvas)  # Add the canvas to the map area or another part of the layout

        # Setup for results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Algorithm", "Total Distance", "Path"])
        map_area.addWidget(self.results_table)

        # Add layouts to main layout
        main_layout.addLayout(map_area, 75)  # Map area takes 75% of the horizontal space
        main_layout.addLayout(sidebar, 25)   # Sidebar takes 25% of the horizontal space

        self.show_map()
       

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # Main horizontal layout

        # Applying a global style to the application that works well with both light and dark themes
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;  # Light grey background
                color: #000000;  # Black text
            }
            QLabel, QComboBox, QListWidget, QPushButton {
                background-color: #ffffff;  # White background for input and labels
                color: #000000;  # Black text
            }
        """)

        # Sidebar for input controls
        sidebar = QVBoxLayout()
        start_city_label = QLabel("Starting City")
        sidebar.addWidget(start_city_label)
        self.start_city_dropdown = QComboBox()
        self.start_city_dropdown.addItems(['Los Angeles', 'San Diego', 'Irvine', 'Santa Ana', 'Long Beach', 'Pasadena', 'Malibu', 'Ventura', 'Riverside', 'Bakersfield', 'Anaheim', 'Santa Barbara'])
        sidebar.addWidget(self.start_city_dropdown)

        destination_label = QLabel("Delivery Locations")
        sidebar.addWidget(destination_label)
        self.destination_cities_list = QListWidget()
        self.destination_cities_list.addItems(['Los Angeles', 'San Diego', 'Irvine', 'Santa Ana', 'Long Beach', 'Pasadena', 'Malibu', 'Ventura', 'Riverside', 'Bakersfield', 'Anaheim', 'Santa Barbara'])
        self.destination_cities_list.setSelectionMode(QListWidget.MultiSelection)
        sidebar.addWidget(self.destination_cities_list)

        self.algorithm_selection = QComboBox()
        self.algorithm_selection.addItems(['Greedy', 'Nearest Neighbor', 'Random Sampling', 'Genetic Algorithm', 'Ant Colony Optimization'])
        sidebar.addWidget(self.algorithm_selection)

        self.calculate_button = QPushButton('Calculate Route')
        self.calculate_button.clicked.connect(self.calculate_route)
        sidebar.addWidget(self.calculate_button)

        self.execute_all_button = QPushButton('Execute All')
        self.execute_all_button.clicked.connect(self.execute_all_algorithms)
        sidebar.addWidget(self.execute_all_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_app)
        sidebar.addWidget(self.refresh_button)

        # # Scroll Area Configuration
        # scroll_area = QScrollArea()
        # scroll_area.setWidgetResizable(True)
        # scroll_content = QWidget()
        # scroll_area.setWidget(scroll_content)
        # map_area = QVBoxLayout(scroll_content)  # Put the map_area inside the scrollable content

        # self.map_view = QWebEngineView()
        # map_area.addWidget(self.map_view)

        # self.route_label = QLabel("Route will be displayed here.")
        # self.route_label.setMaximumHeight(30)
        # self.route_label.setStyleSheet("padding: 5px;")
        # map_area.addWidget(self.route_label)

        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)
        # map_area.addWidget(self.canvas)

        # self.results_table = QTableWidget()
        # self.results_table.setColumnCount(3)
        # self.results_table.setHorizontalHeaderLabels(["Algorithm", "Total Distance", "Path"])
        # map_area.addWidget(self.results_table)

        # # Adding the scroll area to the main layout
        # main_layout.addWidget(scroll_area, 75)  # The scroll area now takes up the main part of the layout
        # main_layout.addLayout(sidebar, 25)  # Sidebar remains the same

        # self.show_map()
        # Scroll Area Configuration
        # Scroll Area Configuration
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        map_area = QVBoxLayout(scroll_content)  # Put the map_area inside the scrollable content

        self.map_view = QWebEngineView()
        self.map_view.setFixedHeight(300)  # Optionally set fixed height
        map_area.addWidget(self.map_view)

        self.route_label = QLabel("Route will be displayed here.")
        self.route_label.setMaximumHeight(30)  # Fixed maximum height for the route label
        self.route_label.setStyleSheet("padding: 5px;")
        map_area.addWidget(self.route_label)

        # Adding the table before the graph in the layout
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Algorithm", "Total Distance", "Path"])
        self.results_table.setFixedHeight(300)  # Optionally set fixed height
        map_area.addWidget(self.results_table)

        # Setup for matplotlib chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedHeight(200)  # Optionally set fixed height
        map_area.addWidget(self.canvas)

        # Adding the scroll area to the main layout
        main_layout.addWidget(scroll_area, 75)  # The scroll area takes up the main part of the layout
        main_layout.addLayout(sidebar, 25)  # Sidebar remains the same

        self.show_map()

    def show_map(self):
        # Initialize a folium map with zoom controls
        self.map = folium.Map(location=[34.0522, -118.2437], zoom_start=8, zoom_control=True)
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.map_view.setHtml(data.getvalue().decode())

    def calculate_route(self):

        if not self.destination_cities_list.selectedItems():
            QMessageBox.warning(self, "Selection Required", "Please select at least one city in 'Delivery Locations'.")
            return  # Return early if no cities are selected
    
        city_coords = {
                'Los Angeles': (34.0522, -118.2437),
                'San Diego': (32.7157, -117.1611),
                'Irvine': (33.6846, -117.8265),
                'Santa Ana': (33.7455, -117.8677),
                'Long Beach': (33.7701, -118.1937),
                'Pasadena': (34.1478, -118.1445),
                'Malibu': (34.0259, -118.7798),
                'Ventura': (34.2746, -119.2290),
                'Riverside': (33.9533, -117.3962),
                'Bakersfield': (35.3733, -119.0187),
                'Anaheim': (33.8366, -117.9143),
                'Santa Barbara': (34.4208, -119.6982)
            }
        cities = [self.start_city_dropdown.currentText()] + [item.text() for item in self.destination_cities_list.selectedItems()]

        n = len(cities)
        dist_matrix = np.zeros((n, n))
        geometries = [[None] * n for _ in range(n)]  # Correct initialization

        selected_algorithm = self.algorithm_selection.currentText()

        for i in range(n):
            for j in range(i + 1, n):
                dist, geom = get_osrm_route(city_coords[cities[i]], city_coords[cities[j]])
                dist_matrix[i][j] = dist_matrix[j][i] = dist
                geometries[i][j] = geometries[j][i] = geom  # Store geometries symmetrically



                if selected_algorithm == 'Greedy':
                    route_indices, cost = solve_tsp_greedy(dist_matrix)
                elif selected_algorithm == 'Nearest Neighbor':
                    route_indices, cost = solve_tsp_nearest_neighbor(dist_matrix)
                elif selected_algorithm == 'Random Sampling':
                    route_indices, cost = solve_tsp_random_sampling(dist_matrix)
                elif selected_algorithm == 'Genetic Algorithm':
                    route_indices, cost = solve_tsp_genetic_algorithm(dist_matrix)
                elif selected_algorithm == 'Ant Colony Optimization':
                    route_indices, cost = solve_tsp_ant_colony_optimization(dist_matrix)


        route = [cities[i] for i in route_indices]

        cost_in_miles = cost * 0.000621371 # to convert mtrs into miles

        route_text = " --> ".join(route) + f" | Total Distance: {cost_in_miles:.2f} miles"

        self.update_map_and_label(route, city_coords, route_text, geometries)

    def execute_all_algorithms(self):
       
        algorithms = {
            'Greedy': solve_tsp_greedy,
            'Nearest Neighbor': solve_tsp_nearest_neighbor,
            'Random Sampling': solve_tsp_random_sampling,
            'Genetic Algorithm': solve_tsp_genetic_algorithm,
            'Ant Colony Optimization': solve_tsp_ant_colony_optimization
        }
        results = []
        times = []
        names = []

        if not self.destination_cities_list.selectedItems():
            QMessageBox.warning(self, "Selection Required", "Please select at least one city in 'Delivery Locations'.")
            return  # Return early if no cities are selected
    
        city_coords = {
                'Los Angeles': (34.0522, -118.2437),
                'San Diego': (32.7157, -117.1611),
                'Irvine': (33.6846, -117.8265),
                'Santa Ana': (33.7455, -117.8677),
                'Long Beach': (33.7701, -118.1937),
                'Pasadena': (34.1478, -118.1445),
                'Malibu': (34.0259, -118.7798),
                'Ventura': (34.2746, -119.2290),
                'Riverside': (33.9533, -117.3962),
                'Bakersfield': (35.3733, -119.0187),
                'Anaheim': (33.8366, -117.9143),
                'Santa Barbara': (34.4208, -119.6982)
            }
        cities = [self.start_city_dropdown.currentText()] + [item.text() for item in self.destination_cities_list.selectedItems()]

        n = len(cities)
        dist_matrix = np.zeros((n, n))
        geometries = [[None] * n for _ in range(n)]  # Correct initialization


        for name, func in algorithms.items():
            
            for i in range(n):
                for j in range(i + 1, n):
                    dist, geom = get_osrm_route(city_coords[cities[i]], city_coords[cities[j]])
                    dist_matrix[i][j] = dist_matrix[j][i] = dist
                    geometries[i][j] = geometries[j][i] = geom  # Store geometries symmetrically
                    
                    start_time = time.time()
                    route_indices, cost = func(dist_matrix)  # Assume dist_matrix is predefined or setup similarly
                    end_time = time.time()

            route = [cities[i] for i in route_indices]
            cost_in_miles = cost * 0.000621371 # to convert mtrs into miles
            cost_in_miles = "{:.2f}".format(cost_in_miles)

            results.append((name, cost_in_miles, ' -> '.join(map(str, route))))
            times.append(end_time - start_time)
            names.append(name)

        self.plot_times(names, times)
        self.update_results_table(results)

    def plot_times(self, names, times):
        self.figure.clear()
        plt.bar(names, times, color='blue')
        plt.ylabel('Execution Time (s)')
        plt.title('Algorithm Execution Times')
        self.canvas.draw()

    def update_results_table(self, results):
        self.results_table.setRowCount(len(results))
        for i, (name, cost, path) in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(name))
            self.results_table.setItem(i, 1, QTableWidgetItem(str(cost)))
            self.results_table.setItem(i, 2, QTableWidgetItem(path))

    def update_map_and_label(self, route, city_coords, route_text, geometries):
        m = folium.Map(location=city_coords[route[0]], zoom_start=8)
        for i in range(len(route)-1):
            start_city = route[i]
            end_city = route[i+1]
            start_coords = city_coords[start_city]
            end_coords = city_coords[end_city]
            folium.Marker(start_coords, popup=start_city).add_to(m)

            # Ensure geometry data is not None before decoding
            route_geometry = geometries[route.index(start_city)][route.index(end_city)]
            if route_geometry:
                route_path = polyline.decode(route_geometry)
                folium.PolyLine(locations=route_path, color='blue', weight=5).add_to(m)
            else:
                print(f"No route geometry available from {start_city} to {end_city}")

        # Close the loop to the start city
        folium.Marker(end_coords, popup=route[0]).add_to(m)
        route_geometry = geometries[route.index(route[-1])][route.index(route[0])]
        if route_geometry:
            route_path = polyline.decode(route_geometry)
            folium.PolyLine(locations=route_path, color='blue', weight=5).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_view.setHtml(data.getvalue().decode())
        self.route_label.setText(route_text)

    def refresh_app(self):
        # Clear selections
        self.start_city_dropdown.setCurrentIndex(0)
        self.destination_cities_list.clearSelection()

        # Reset map and label
        self.show_map()
        self.route_label.setText("Route will be displayed here.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TSPMapApp()
    ex.show()
    sys.exit(app.exec_())
