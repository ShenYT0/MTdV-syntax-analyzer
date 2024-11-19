'''
TM Turning Machine tokenizer and parser.
Author: Siman Chen, Yuntian Shen

règles de MTdV:
I	affiche l’état de la machine
P	« pause », interrompt temporairement l’exécution du programme ; celle-ci reprend une fois que l’utilisateur a tapé sur une touche du clavier en réponse au prompt affiché.
G, D	déplace la tête de lecture respectivement d’une position à Gauche, à Droite
0, 1	écrit respectivement un 0 (case vide) ou un 1 (bâton) à l’emplacement de la tête de lecture
si (0) x1 x2 … }	si la tête de lecture est sur une case vide alors les instructions x1, x2, … sont exécutées en séquence, sinon exécute la première instruction qui suit l’accolade fermante }
si (1) x1 x2 … }	même chose dans le cas où la tête de lecture est positionnée sur un bâton
boucle x1 x2 … }	répète la séquence d’instructions x1 x2 …, jusqu’à ce que l’une d’elle soit l’instruction fin
fin	rompt le cycle de répétition d’une boucle en faisant exécuter la première instruction qui suit l’accolade fermante de la première boucle contenant l’instruction fin ; si fin n’est contenue dans aucune boucle alors le programme s’arrête.
%	définit une ligne de commentaire non exécutable
#	marqueur de fin de fichier requis comme dernière instruction
'''

import argparse
import chardet
from dataclasses import dataclass
import json
import os
import pygraphviz as pgv
import re
from typing import List, Tuple

@dataclass
class Node:
	id: int
	inst: str # instruction
	edges: List[Tuple[int, str]] # (to_node_id, condition)

class MTdV:
	tokens: List[str]
	nodes: List[Node]

	def __init__(self, text: str):
		self.tokens = MTdV.tokenize(text)
		self.nodes = MTdV.parse(self.tokens)

	def tokenize(text: str) -> List[str]:
		'''
		Tokenize the input text into a list of tokens.
		:param text: input text
		:return: list of tokens
		'''
		# split lines
		text = re.split(r"\r\n|\n", text)

		tokens = []
		for line in text:
			
			# sometimes, } is not separated from its previous word
			line = re.sub("}", " } ", line)
			line = re.sub("\(", " (", line)
			# remove extra spaces between parentheses
			line = re.sub(r'\(\s+', '(', line)
			line = re.sub(r'\s+\)', ')', line)

			no_comment_part = []
			for part in line.split():
				part = part.strip()
				if part[0] == '%':
					break
					# ignore comment lines or inline comments
				no_comment_part.append(part)
			no_comment_line = " ".join(no_comment_part)

			# split by space, except for the case of "si (0)"
			for token in re.findall(r'((si \((0|1)\))|[^ ]+)', no_comment_line):
				tokens.append(token[0])
		return tokens


	def parse(tokens: List[str]) -> List[Node]:
		'''
		Parse the list of tokens into a list of nodes.
		:param tokens: list of tokens
		:return: list of nodes
		'''
		nodes = []
		current_node_id = 0
		last_condition = None

		# create a stack to verify if the } is well closed
		stack = []
		stack_b = [] # stack for boucle
		
		nodes.append(Node(id=current_node_id, inst='start', edges=[]))

		file_end = False
		
		for token in tokens:
			# use condition to store the condition of the last if or loop
			condition = ''
			if last_condition == "if_begin":
				condition = "true"
			elif last_condition == "if_end":
				condition = "false"
			elif last_condition == "loop_begin":
				condition = "start loop"
			elif last_condition == "loop_end":
				condition = "end loop"

			
			if token in ['I', 'P', 'G', 'D', '0', '1']:
				if token == 'I':
					inst = 'print machine state'
				elif token == 'P':
					inst = 'pause'
				elif token in ['G', 'D']:
					inst = f"move {'left' if token == 'G' else 'right'}"
				elif token in ['0', '1']:
					inst = f'write {token}'

				new_node_id = len(nodes)
				nodes[current_node_id].edges.append((new_node_id, condition))
				last_condition = None
				nodes.append(Node(id=new_node_id, inst=inst, edges=[]))

				current_node_id = new_node_id
			elif token in ['si (0)', 'si (1)', 'boucle']:
				if token == 'boucle':
					inst = "loop"
					last_condition = "loop_begin"

					new_node_id = len(nodes)
					nodes[current_node_id].edges.append((new_node_id, condition))
					nodes.append(Node(id=new_node_id, inst=inst, edges=[]))

					stack.append((token, new_node_id))
					stack_b.append(new_node_id)

					current_node_id = new_node_id
				else :
					inst = f'if read {token[-2]}'

					last_condition = "if_begin"
					new_node_id = len(nodes)
					
					nodes[current_node_id].edges.append((new_node_id, condition))
					nodes.append(Node(id=new_node_id, inst=inst, edges=[]))

					stack.append((token, new_node_id))

					current_node_id = new_node_id

			elif token == 'fin':
				if stack_b:
					id_ = stack_b[-1]
					nodes[current_node_id].edges.append((id_, 'break'))
				else:
					new_node_id = len(nodes)
					nodes[current_node_id].edges.append((new_node_id, 'program finished'))
					nodes.append(Node(id=new_node_id, inst='finish', edges=[]))
			elif token == '}':
				if stack:
					token_, id_ = stack.pop()
					if token_ in ['si (0)', 'si (1)']:
						last_condition = "if_end"
						if current_node_id != id_:
							nodes[current_node_id].edges.append((id_, condition))
						current_node_id = id_
					else :
						last_condition = "loop_end"
						stack_b.pop()
						nodes[current_node_id].edges.append((id_, 'continue'))
						current_node_id = id_
				else:
					raise ValueError(f"Unmatched }}")
			elif token == '#':
				new_node_id = len(nodes)
				nodes[current_node_id].edges.append((new_node_id, 'end of file'))
				nodes.append(Node(id=new_node_id, inst='end', edges=[]))
				file_end = True
				break
			else:
				raise ValueError(f"Unknown token: {token}")

		if not file_end:
			raise ValueError(f"Missing end of file token")
		
		return nodes
	
	def generate_json(self, filename: str):
		'''
		Generate a json file from the list of nodes.
		:param filename: output filename
		'''
		data = {}
		data['nodes'] = []
		for node in self.nodes:
			data['nodes'].append({
				'id': node.id,
				'inst': node.inst,
				'edges': node.edges
			})
		with open(filename + '.json', 'w') as f:
			json.dump(data, f, indent=4)
	
	def generate_graph(self, filename: str):
		'''
		Generate a graph from the list of nodes.
		:param filename: output filename
		'''
		G = pgv.AGraph(directed=True)
		for node in self.nodes:
			for edge in node.edges:
				G.add_edge(f"{node.id} {node.inst}", f"{edge[0]} {self.nodes[edge[0]].inst}", label=edge[1])
		G.layout(prog='dot')
		G.draw(filename)

def main():
	'''
	Parser for Turing Machine instructions by Mr. Claude del Vigna
	Stores the instructions in a json file and generates a graph to visualize the instructions.
	'''
	parser = argparse.ArgumentParser(description='TM tokenizer')
	parser.add_argument('input', type=str, help='input file')
	parser.add_argument('-o', '--output', type=str, help='output file')
	args = parser.parse_args()

	input_filename, input_extension = os.path.splitext(os.path.basename(args.input))

	if not args.output:
		output_path = input_filename
	else:
		output_path = args.output + '/' + input_filename

	with open(args.input, 'r', encoding="iso-8859-1") as f:
		text = f.read()
		mtdv = MTdV(text)
		# print(mtdv.tokens)
		# print(mtdv.nodes)
		mtdv.generate_json(output_path)
		mtdv.generate_graph(output_path + '.png')
	return

if __name__ == "__main__":
	main()