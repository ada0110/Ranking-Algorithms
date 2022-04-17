import sys
sys.path.insert(0, ".")
sys.path.insert(0, "..")

from graph import Graph


# constants
ITERATION = 100
DAMPING_FACTOR = 0.85


def page_rank(graph, d, iteration=100):
    for i in range(iteration):
        page_rank_iter(graph, d)
        
    
def page_rank_iter(graph, d):
    node_list = graph.nodes
    for node in node_list:
        node.update_pagerank(d, len(graph.nodes))
        
    # normalize outgoing links
    # overall idea: if you refer more people, each referal has less value
    graph.normalize_pagerank()
    # print(graph.get_pagerank_list())
    # print()


if __name__ == '__main__':

    input_file = './dataset/graph_iiit.txt'
    
    # build graph
    with open(input_file) as f:
        lines = f.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)

    graph.sort_nodes()
    print(graph.display())

    # run page_rank algo
    page_rank(graph, DAMPING_FACTOR, iteration=ITERATION)
    page_rank_list = graph.get_pagerank_list()
    
    print("page ranks:")
    for i, score in enumerate(page_rank_list):
        print(i, score)
    
    
