from src.network_manager import NetworkManager
from src.model_logic import PCenterSolver
from src.visualizer import MapVisualizer

def main():
    # Initialize network manager and load map data
    # Added 'CI' to all filenames to match your directory structure
    PROVINCE_CSV = {
        "Alberta":                  "data/PopulationData/98-401-X2021006CI_English_CSV_data_Prairies.csv",
        "British Columbia":         "data/PopulationData/98-401-X2021006CI_English_CSV_data_BritishColumbia.csv",
        "Manitoba":                 "data/PopulationData/98-401-X2021006CI_English_CSV_data_Prairies.csv",
        "New Brunswick":            "data/PopulationData/98-401-X2021006CI_English_CSV_data_Atlantic.csv",
        "Newfoundland and Labrador":"data/PopulationData/98-401-X2021006CI_English_CSV_data_Atlantic.csv",
        "Northwest Territories":    "data/PopulationData/98-401-X2021006CI_English_CSV_data_Territories.csv",
        "Nova Scotia":              "data/PopulationData/98-401-X2021006CI_English_CSV_data_Atlantic.csv",
        "Nunavut":                  "data/PopulationData/98-401-X2021006CI_English_CSV_data_Territories.csv",
        "Ontario":                  "data/PopulationData/98-401-X2021006CI_English_CSV_data_Ontario.csv",
        "Prince Edward Island":     "data/PopulationData/98-401-X2021006CI_English_CSV_data_Atlantic.csv",
        "Quebec":                   "data/PopulationData/98-401-X2021006CI_English_CSV_data_Quebec.csv",
        "Saskatchewan":             "data/PopulationData/98-401-X2021006CI_English_CSV_data_Prairies.csv",
        "Yukon":                    "data/PopulationData/98-401-X2021006CI_English_CSV_data_Territories.csv",
    }
    
    place_input = input("Please enter a Canadian city (e.g. Coaldale, Alberta): ")
    place = place_input + ", Canada"
    
    # Split by comma and extract the province name
    parts = place_input.split(",")
    if len(parts) < 2:
        raise ValueError("Please provide the city and province (e.g., 'Lethbridge, Alberta')")
    
    province = parts[1].strip()

    pop_path = PROVINCE_CSV.get(province)
    if pop_path is None:
        raise ValueError(f"Unrecognized province: '{province}'. Check spelling and capitalization.")
    
    p_count = int(input("How many Hospitals? "))

    manager = NetworkManager(place)
    graph = manager.load_graph()
    
    # Use the 'pop_path' variable we just looked up instead of the hardcoded string
    demand_weights = manager.load_demand_from_shapefile("data/DAdata/lda_000b21a_e.shp", pop_path)
    demand_nodes = list(demand_weights.keys())
    distances = manager.compute_distances(demand_nodes)
    print(f"done with distance")
    # Solve p-center problem to locate facilities
    # p_count = # of Hospitals
    solver = PCenterSolver(demand_nodes, distances, p_count=p_count, weights=demand_weights)
    hospitals, max_dist = solver.solve()


    # Print optimization status and facility locations
    print(f"\nStatus: Optimal")
    print(f"Maximized Equity Distance: {max_dist:.3f} meters")
    for i, h in enumerate(hospitals, 1):
        print(f"Hospital {i} Location (Node ID): {h}")

    # Generate and save spatial visualization
    viz = MapVisualizer(graph)
    viz.save_map(hospitals, filename=f"images/{place}_p={p_count}.png")

if __name__ == "__main__":
    main()