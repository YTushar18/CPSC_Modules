import sys
import requests
import folium
import polyline
import io
import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QListWidget, QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
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
        self.setGeometry(100, 100, 1280, 720)
        self.initUI()

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

        self.destination_cities_list = QListWidget()
        destination_label = QLabel("Delivery Locations")
        sidebar.addWidget(destination_label)
        self.destination_cities_list.addItems(['Los Angeles', 'San Diego', 'Irvine', 'Santa Ana', 'Long Beach', 'Pasadena', 'Malibu', 'Ventura', 'Riverside', 'Bakersfield', 'Anaheim', 'Santa Barbara'])
        self.destination_cities_list.setSelectionMode(QListWidget.MultiSelection)
        sidebar.addWidget(self.destination_cities_list)

        self.calculate_button = QPushButton('Calculate Route')
        self.calculate_button.clicked.connect(self.calculate_route)
        sidebar.addWidget(self.calculate_button)

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

        # Add layouts to main layout
        main_layout.addLayout(map_area, 75)  # Map area takes 75% of the horizontal space
        main_layout.addLayout(sidebar, 25)   # Sidebar takes 25% of the horizontal space

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

        for i in range(n):
            for j in range(i + 1, n):
                dist, geom = get_osrm_route(city_coords[cities[i]], city_coords[cities[j]])
                dist_matrix[i][j] = dist_matrix[j][i] = dist
                geometries[i][j] = geometries[j][i] = geom  # Store geometries symmetrically



                print("Distance Matrix:")
                print(dist_matrix)
                route_indices, cost = solve_tsp_greedy(dist_matrix)
                print("Route:", route_indices)
                print("Cost of the route:", cost)
                
                
                # route_indices, cost = solve_tsp(dist_matrix)




        route = [cities[i] for i in route_indices]

        cost_in_miles = cost * 0.000621371 # to convert mtrs into miles

        route_text = " --> ".join(route) + f" | Total Distance: {cost_in_miles:.2f} miles"

        self.update_map_and_label(route, city_coords, route_text, geometries)

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
