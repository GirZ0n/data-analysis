from src.tasks.task3.pages.filtering_page import show_filter_page
from src.tasks.task3.pages.analysis_page import show_analysis_page
from src.tasks.task3.pages.k_means_clustering import show_k_means_clustering_page

PAGE_MAP = {
    'Filtering': show_filter_page,
    'Cluster analysis': show_analysis_page,
    'K-means clustering': show_k_means_clustering_page,
}
