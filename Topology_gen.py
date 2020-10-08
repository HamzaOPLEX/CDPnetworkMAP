import graphviz as gv

class GenTopo :
    def __init__(self):
        self.styles = {
            'graph': {
                'label': 'CDP Network Topology :)',
                'fontsize': '16',
                'fontcolor': 'white',
                'bgcolor': '#333333',
                'rankdir': 'BT',
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'box',
                'fontcolor': 'white',
                'color': '#006699',
                'style': 'filled',
                'fillcolor': '#006699',
                'margin': '0.3',
            },
            'edges': {
                'style': 'dashed',
                'color': 'green',
                'arrowhead': 'open',
                'fontname': 'Courier',
                'fontsize': '11',
                'fontcolor': 'white',
            }}


    def apply_styles(self,graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )
        return graph


    def draw_topology(self,topology_dict, output_filename='topologys/topology'):


        nodes = set([key[0] for key in list(topology_dict.keys()) + list(topology_dict.values())])

        g1 = gv.Graph(format='png')

        for node in nodes:
            g1.node(node)

        for key, value in topology_dict.items():
            head, t_label = key
            tail, h_label = value
            g1.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" "*12)
        g1 = self.apply_styles(g1, self.styles)
        filename = g1.render(filename=output_filename)
        print(("Graph saved in", filename))


if __name__ == '__main__' :

    diag5 = {('R2', 'Fa0/0'): ('R3', 'Fa0/0'), ('R4', 'Fa1/0'): ('R2', 'Fa1/0'), ('R2', 'Fa1/0'): ('R1', 'Fa0/1'), ('R2', 'Fa3/0'): ('R1', 'Fa3/0'), ('R3', 'Fa0/1'): ('R1', 'Fa0/1'), ('R4', 'Fa4/0'): ('R1', 'Fa4/0'), ('R5', 'Fa0/1'): ('R4', 'Fa0/1'), ('R5', 'Fa4/0'): ('R3', 'Fa3/0')}

    draw = GenTopo()

    draw.draw_topology(diag5)