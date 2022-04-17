import time
from argparse import ArgumentParser
from collections import deque
from get_page_links import get_page_links


MAX_DEPTH = 2
MAX_LINKS = 1000
MAX_LINK_PER_PAGE = 50
VERBOSE = True
adj_list = []
visited = set()

 
def bfs_traversal(current_url, base_url):
    queue = deque()
    link_count = 1
    
    queue.append((current_url, 1))
    visited.add(current_url)
    
    while(queue):
        current_url, depth = queue.popleft()
        
        if depth > MAX_DEPTH or link_count > MAX_LINKS:
            return adj_list
        
        page_links = get_page_links(current_url, base_url)
        print(f"src: {current_url} | num links: {len(page_links)}")
   
        for link in list(page_links)[:MAX_LINK_PER_PAGE]:
            adj_list.append([current_url, link])
            tab_space = " "*depth
            
            # skip if link is already added to queue
            if link in visited:
                if VERBOSE:
                    print(f'{tab_space} depth: {depth} | skipped: {link}')
                continue
            
            queue.append((link, depth+1))
            # add to visited
            visited.add(link)
            link_count += 1
            
            if VERBOSE:
                print(f'{tab_space} depth: {depth} | added: {link}')
                            

# dfs version
def dfs_traversal(current_url, base_url, depth):
    if depth > MAX_DEPTH:
        return
    
    # add to visted
    visited.add(current_url)
    
    page_links = get_page_links(current_url, base_url)
    print(f"src: {current_url} | num links: {len(page_links)}")
    
    for link in list(page_links)[:MAX_LINK_PER_PAGE]:
        adj_list.append([current_url, link])
        if link not in visited:
            if VERBOSE:
                tab_space = "  "*depth
                print(f'{tab_space}depth: {depth} | url: {link}')
            # recursive call
            dfs_traversal(link, base_url, depth + 1)
            
            

if __name__ == '__main__':
    # read arguments
    parser = ArgumentParser()
    
    parser.add_argument('-p', '--page_url',
                         default= 'https://www.iiit.ac.in/')
    parser.add_argument('-b', '--base_url',
                         default= 'https://www.iiit.ac.in/')
    parser.add_argument('-o', '--output_file',
                         default= 'crawled.txt')
    
    parser = parser.parse_args()
    
    # get links on page
    print(f"fetching from page: {parser.page_url} | base: {parser.base_url}")
    
    start = time.time()
    bfs_traversal(parser.page_url, parser.base_url)
    
    print("="*60)
    print(f"MAX_DEPTH: {MAX_DEPTH} | MAX_LINK_PER_PAGE: {MAX_LINK_PER_PAGE}")
    print(f"total edges found: {len(adj_list)}")
    print(f"time taken: {time.time() - start: .2f} sec")
    
    with open(parser.output_file, "w") as op:
        for u,v in adj_list:
            op.write(f"{u}\t{v}\n")
    
    print(f"edge list written to: {parser.output_file}")
    
    