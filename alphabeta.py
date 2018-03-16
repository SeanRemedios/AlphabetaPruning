import math

'''
 ' File Class to handle the reading and writing to files
'''
class File:
	'''
	 ' Constructor for File class
	 '
	 ' Input:	fileRead - The file to read from
	 '			fileWrite - The file to write to
	'''
	def __init__(self, fileRead, fileWrite):
		self.fileRead = open(fileRead,"r")
		# Empty the contents before opening the appending file
		open(fileWrite, "w").close()
		self.fileWrite = open(fileWrite, "a")


	'''
	 ' Read two sets from a file (same line) for each line and return
	 ' it as a tree 
	 '
	 ' Input:	None
	 '
	 ' Output:	tree - Two sets of data
	'''
	def readFile(self):
		# Split on new lines
		tree = self.fileRead.read().splitlines()
		return tree


	'''
	 ' Write a list to a file
	 '
	 ' Input:	data - [insert something useful]
	 '
	 ' Output:	None
	'''
	def writeFile(self, data):
		# Add a newline at the end of the line so each solution
		# goes on a new line
		self.fileWrite.write(data + "\n")


	'''
	 ' Close the files
	 '
	 ' Input:	None
	 '
	 ' Output:	None
	'''
	def closeFile(self, fileToClose):
		fileToClose.close()


'''
 ' The Tree class contains the functions to split the input into tuples,
 ' and get the other lists (Min nodes, Max nodes, root).
'''
class Tree(object):
	'''Tree'''
	def __init__(self):
		super(Tree, self).__init__()		


	'''
	 ' Get the literal tree structure from the input. The input is now
	 ' tuples with characters as the first index and the connecting edge
	 ' as the second. If the second index is a number, it is an integer.
	 ' MINMAX nodes are tuples of 2 strings.
	 '
	 ' Input:	treeInput - The input read from the file
	 '
	 ' Output:	treeLit - The tree set up properly
	'''
	def splitNodes(self, treeInput):
		treeRep = treeInput.replace('{', '') # Remove starting braces
		treeRep = treeRep.replace(' ', '') # Remove the space 
		treeSpl = treeRep.split('}') # Split on ending brace (between sets)
		treeSpl.remove('') # Remove no string (since second set has '}')

		treeLit = [] # Full list (2 parts)
		for part in treeSpl:
			treeTemp = []
			splitPart = part.split('),(') # Split on tuples
			for sPart in splitPart: # Each part
				# Remove the braces so we can just deal with the elements
				replacedPart = sPart.replace('(', '').replace(')', '') \
									.replace(']', '').replace('[', '')
				# Split on the commas
				partLis = replacedPart.split(',')
				if not partLis[1].isalpha(): # Look for the integers (leaves)
					tuplePart = (partLis[0], int(partLis[1]))
				else:
					tuplePart = (partLis[0], partLis[1])
				treeTemp.append(tuplePart)
			treeLit.append(treeTemp)

		return treeLit


	'''
	 ' Returns the root of the tree, always the first element in the
	 ' first list.
	 '
	 ' Input:	tree - The tree lists
	 '
	 ' Output:	The root of the tree
	'''
	def getRoot(self, tree):
		return tree[0][0] # Root is first node in first set


	'''
	 ' Returns a list of node values depending on the type requested
	 ' specified by 'typeMinMax'. Finds the Min or Max node lists
	 ' 
	 ' Input:	tree - The tree lists
	 ' 			typeMinMax - A string specifying 'MIN' or 'MAX'
	 '
	 ' Output:	nodes - The list of nodes specifying to typeMinMax
	'''
	def getMinMaxNodes(self, tree, typeMinMax):
		min_max_Nodes = tree[0]

		nodes = []
		# List comprehension is faster than normal for loop
		[nodes.append(node[0]) for node in min_max_Nodes if node[1] == typeMinMax]

		return nodes


'''
 ' The AlphaBeta class uses the alpha-beta pruning algorithm to find the
 ' value of the tree.
'''
class AlphaBeta(object):
	'''AlphaBeta'''
	def __init__(self, root, allnodes, maxNodes, minNodes):
		super(AlphaBeta, self).__init__()
		self.root = root
		self.allnodes = allnodes # All nodes with edges
		self.maxNodes = maxNodes # All max nodes
		self.minNodes = minNodes # All min nodes
		self.leafNodesExamined = 0 # Number of leaf nodes examined


	'''
	 ' Function uses the alpha-beta pruning algorithm to find a value of the tree
	 ' 
	 ' Input: 	current_node - Current node being examined
	 ' 			alpha - Current alpha value
	 '			beta - Current beta value
	 '
	 ' Output:	value of the tree found by the alpha-beta algorithm
	'''
	def alpha_beta(self, current_node, alpha, beta):
		if current_node == self.root: # If the node is root, set to infinity
			alpha = -math.inf # -infinity because we compare alpha >= beta
			beta = math.inf

		# We can do this because only leaf nodes have integer values
		if type(current_node) == int: # Leaf node
			self.leafNodesExamined += 1 # Count leaf nodes 
			return current_node

		if current_node in self.maxNodes: # If it's a max node
			# current_node is just a value
			# allnodes contains (nodeValue, childNode) so we iterate through
			# the list to find the childNode where the nodeValue matches
			# the current_node
			for childMax in self.allnodes: 
				if childMax[0] == current_node: # nodeValue = current_node
					# Look for max between alpha and rest
					# childMax[1] is child node
					# Max Kaos
					alpha = max(alpha, self.alpha_beta(childMax[1], alpha, beta))
					if alpha >= beta: # Cut off the rest of the child
						return alpha
			return alpha

		if current_node in self.minNodes: # If it's a min node
			for childMin in self.allnodes: 
				if childMin[0] == current_node[0]:
					# Look for min between beta and rest
					# childMax[1] is child node
					# Min Kaos
					beta = min(beta, self.alpha_beta(childMin[1], alpha, beta))
					if beta <= alpha: # Cut off rest of the child
						return beta
			return beta

		print("Error: Invalid Node") # How the hell did we reach here?


def main():
	READFILE = "alphabeta.txt"
	WRITEFILE = "alphabeta_out.txt"

	# Open the file stuff and read it
	fl = File(READFILE, WRITEFILE)
	trees = fl.readFile()
	fl.closeFile(fl.fileRead)

	treeClass = Tree()
	countGraph = 0
	for eachTree in trees: # Each tree (line) from input
		countGraph += 1 # Count the graph number

		tree = treeClass.splitNodes(eachTree) # Split the input into parts
		root = treeClass.getRoot(tree)  # Get the root node
		# Get the MAX node list
		maxNodes = treeClass.getMinMaxNodes(tree, 'MAX')
		# Get the MIN node list
		minNodes = treeClass.getMinMaxNodes(tree, 'MIN')

		# Instantiate the class
		alphabetaClass = AlphaBeta(root, tree[1], maxNodes, minNodes)
		# root[0] because we just want the value
		# initiate with -inf and +inf, we do this anyway in the alg
		result = alphabetaClass.alpha_beta(root[0], -math.inf, math.inf)

		# Put the results into a string
		stringOut = "Graph %d: Score: %d; Leaf Nodes Examined: %d" % \
			(countGraph, result, alphabetaClass.leafNodesExamined)
		print(stringOut)
		# Write to a file
		fl.writeFile(stringOut)
	fl.closeFile(fl.fileWrite) # Close after all writing is done


if __name__ == '__main__':
	main()
