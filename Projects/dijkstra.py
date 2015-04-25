def graph(nodes):
	return {node: {} for node in nodes}

def edge(graph, n1, n2, weight):
	graph[n1][n2]=weight
	graph[n2][n1]=weight

def Dijkstra(G, start, end=None):
	op = {} # open
	cl = {} # closed
	op[start] = [0, None] #node, movement cost, parent
	
	def pick_op():
		return min(op, key=lambda n: op[n][0])

	while len(op):
		n = pick_op()
		neighbors = {nei:G[n][nei] for nei in G[n] if nei not in cl}

		for nei in neighbors:
			if nei in op:
				if op[nei][0] > op[n][0]+neighbors[nei]:
					op[nei][0] = op[n][0]+neighbors[nei]
					op[nei][1] = n
			else:
				op[nei] = [op[n][0]+neighbors[nei], n]
		cl[n] = op[n]
		del op[n]

		if end and end in cl:
			out = []
			parent = cl[end][1]
			current = end
			while current:
				out.append(current)
				current = cl[current][1]
			return out
	return cl


if __name__ == '__main__':
	g = graph("abcdefgh")
	edge(g,'f','a',1)
	edge(g,'f','e',2)
	edge(g,'e','a',2)
	edge(g,'a','b',1)
	edge(g,'b','g',1)
	edge(g,'b','c',2)
	edge(g,'g','h',0.5)
	edge(g,'h','d',0.5)
	edge(g,'c','d',1)
	edge(g,'d','e',1)

	print Dijkstra(g, 'g', 'f')
