import osmnx as ox
import networkx as nx
import random
import geopandas as gpd
import pyproj
import pandas as pd
from shapely.geometry import box
from tqdm import tqdm

class NetworkManager:
    def __init__(self, city_name, network_type="drive"):
        # Store location and network constraints
        self.city_name = city_name
        self.network_type = network_type
        self.graph = None
        self.nodes = []

    def load_graph(self):
        # Download road network from OpenStreetMap
        print(f"--- Loading map for {self.city_name} ---")
        self.graph = ox.graph_from_place(self.city_name, network_type=self.network_type)
        self.nodes = list(self.graph.nodes)
        return self.graph

    def get_sample_distances(self, sample_size=30, seed=None):
        # Sample nodes and calculate travel distances between them
        if seed is not None:
            random.seed(seed)
            
        super_nodes = random.sample(self.nodes, sample_size)
        distance_matrix = {}
        big_m = 999999

        print(f"Calculating shortest paths for {sample_size} sample nodes...")
        
        # Calculate Dijkstra shortest paths for each sample node
        for start_node in tqdm(super_nodes, desc="Pathfinding Progress", unit="node"):
            lengths = nx.single_source_dijkstra_path_length(
                self.graph, 
                start_node, 
                weight='length'
            )
            
            for end_node in super_nodes:
                # Map distances; use penalty for unreachable paths
                dist = lengths.get(end_node, big_m)
                distance_matrix[(start_node, end_node)] = dist
        
        return super_nodes, distance_matrix


    def load_demand_from_shapefile(self, shp_path, pop_path):
        print(f"--- Loading demand data from {shp_path} ---")

        #  Get bounding box of the user's city graph 
        nodes, _ = ox.graph_to_gdfs(self.graph)
        minx, miny, maxx, maxy = nodes.total_bounds

        #  Reproject bbox to match shapefile CRS for spatial filtering 
        shp_crs = pyproj.CRS(gpd.read_file(shp_path, rows=0).crs)
        transformer = pyproj.Transformer.from_crs("EPSG:4326", shp_crs, always_xy=True)
        read_bbox = (*transformer.transform(minx, miny), *transformer.transform(maxx, maxy))

        #  Load only DAs within the city bounds 
        gdf = gpd.read_file(shp_path, bbox=read_bbox).to_crs("EPSG:4326")
        if len(gdf) == 0:
            raise ValueError("No StatsCan data found in this region.")

        #  Join population counts from census profile CSV 
        # CSV is long-format: one row per characteristic per DA, CHARACTERISTIC_ID=1 is total population
        pop_df = (
            pd.read_csv(pop_path, encoding="latin1", usecols=["DGUID", "CHARACTERISTIC_ID", "C1_COUNT_TOTAL"])
            .query("CHARACTERISTIC_ID == 1")[["DGUID", "C1_COUNT_TOTAL"]]
        )
        gdf = gdf.merge(pop_df, on="DGUID", how="left")
        gdf["C1_COUNT_TOTAL"] = gdf["C1_COUNT_TOTAL"].fillna(1)  # fallback for unmatched DAs

        #  Sample up to 200 DAs, weighted by population 
        # Denser areas are more likely to be selected as demand nodes
        if len(gdf) > 200:
            weights = gdf["C1_COUNT_TOTAL"] / gdf["C1_COUNT_TOTAL"].sum()
            gdf = gdf.sample(n=200, random_state=0, weights=weights)

        #  Compute DA centroids (in meters for accuracy, then back to lat/lon) 
        centroids = gdf.to_crs(3857).geometry.centroid.to_crs(4326)

        #  Snap centroids to nearest OSM road network nodes 
        # If multiple DAs snap to the same node, their populations are summed
        demand_weights = {}
        for point, pop in zip(centroids, gdf["C1_COUNT_TOTAL"]):
            node = ox.distance.nearest_nodes(self.graph, X=point.x, Y=point.y)
            demand_weights[node] = demand_weights.get(node, 0) + pop

        print(f"  Found {len(demand_weights)} unique demand nodes.")
        return demand_weights


    def compute_distances(self, nodes):
        print(f"Calculating shortest paths for {len(nodes)} demand nodes...")

        distance_matrix = {}
        big_m = 999999  # penalty distance for unreachable nodes

        #  Run Dijkstra from each demand node to all others 
        # O(n^2) pairs total; single_source_dijkstra_path_length is efficient for sparse graphs
        for start_node in tqdm(nodes, desc="Pathfinding Progress", unit="node"):
            lengths = nx.single_source_dijkstra_path_length(self.graph, start_node, weight='length')
            for end_node in nodes:
                distance_matrix[(start_node, end_node)] = lengths.get(end_node, big_m)

        return distance_matrix