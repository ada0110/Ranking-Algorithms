## PageRank Algo

1. build the web graph dataset  
  `python simple_crawler.py -b https://www.iith.ac.in/ -p https://www.iith.ac.in/`
 
2. covert the urls to edge list using index

3. run pagerank  
`python page_rank.py -i dataset/graph_iith.txt --iteration 100 --damping_factor .85`




