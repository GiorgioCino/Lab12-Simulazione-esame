import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_voti = DAO.getAllVoti()
        self._all_attori = DAO.getAllAttori()
        self._id_map_attore = {}
        for attore in self._all_attori:
            self._id_map_attore[attore.id] = attore

        self._graph = nx.Graph()

    def build_graph(self, voto_iniziale, voto_finale):
        self._graph.clear()
        nodes = DAO.getAllNodes(voto_iniziale, voto_finale, self._id_map_attore)
        self._graph.add_nodes_from(nodes)

        archi = DAO.getAllEdges(voto_iniziale, voto_finale, self._id_map_attore)
        for arco in archi:
            a1 = arco.attore1
            a2 = arco.attore2
            peso = arco.peso

            if self._graph.has_node(a1) and self._graph.has_node(a2):
                self._graph.add_edge(a1, a2, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    #MODO IN CUI SVILUPPO DI PIU IL MODEL
    def pulisci_incasso2(self, incasso):
        if incasso is None:
            return 0

        incasso = incasso.replace("$", "")
        incasso = incasso.replace(",", "")
        incasso = incasso.strip()

        if incasso == "":
            return 0

        return int(incasso)

    def build_graph2(self, voto_iniziale, voto_finale):
        self._graph.clear()

        nodes = DAO.getAllNodes(
            voto_iniziale,
            voto_finale,
            self._id_map_attore
        )

        self._graph.add_nodes_from(nodes)

        righe_archi = DAO.getAllEdgesGrezzi(
            voto_iniziale,
            voto_finale
        )

        pesi_archi = {}

        for id1, id2, incasso_stringa in righe_archi:

            if id1 not in self._id_map_attore:
                continue

            if id2 not in self._id_map_attore:
                continue

            attore1 = self._id_map_attore[id1]
            attore2 = self._id_map_attore[id2]

            if not self._graph.has_node(attore1):
                continue

            if not self._graph.has_node(attore2):
                continue

            incasso = self.pulisci_incasso(incasso_stringa)

            chiave = (attore1, attore2)

            if chiave not in pesi_archi:
                pesi_archi[chiave] = 0

            pesi_archi[chiave] += incasso

        for chiave in pesi_archi:
            attore1, attore2 = chiave
            peso = pesi_archi[chiave]

            self._graph.add_edge(attore1, attore2, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_all_voti(self):
        return list(self._all_voti)

    def get_edges_info(self):
        result = []

        for a1, a2 in self._graph.edges:
            peso = self._graph[a1][a2]["weight"]
            result.append((a1, a2, peso))

        result.sort(key=lambda x: x[2], reverse=True)  #ordino dal peso piu alto al piu basso

        return result[:5]      #prendo i 5 archi di peso maggiore

    def getInfoCompConnessa(self):

        #se volessi solo stampare il numero di componenti connesse
        return nx.number_connected_components(self._graph)  #per contare direttamente il numero di componenti connesse
        #se voglio sapere quanti nodi ci sono in ogni componente:
        componenti = list(nx.connected_components(self._graph))

        if len(componenti) == 0:
            return []

        componente_max = max(componenti, key=len)

        result = []

        for nodo in componente_max:
            grado = self._graph.degree[nodo]
            result.append((nodo, grado))

        result.sort(key=lambda x: x[1], reverse=True)

        return result

    def getComponenteMaggiore(self):
        componenti = list(nx.connected_components(self._graph))

        if len(componenti) == 0:
            return []

        componente_max = max(componenti, key=len)

        result = []

        for nodo in componente_max:
            #grado = self._graph.degree[nodo]
            result.append(nodo)

        #result.sort(key=lambda x: x[1], reverse=True)

        return result

    def grafoCreato(self):
        """
        Controllo semplice per sapere se il grafo è già stato costruito.
        Serve al Controller prima di cercare il percorso.
        """
        return self._graph.number_of_nodes() > 0

    def getCamminoMassimo(self):
        """
        Punto 2.

        Cerca il cammino semplice più lungo del grafo tale che:
        ogni attore successivo abbia età strettamente minore
        dell'attore precedente.

        Esempio valido:
        75 anni -> 60 anni -> 42 anni

        Esempio non valido:
        75 anni -> 80 anni
        """

        # Miglior cammino trovato fino a questo momento
        best_path = []

        # Provo a far partire il cammino da ogni attore del grafo
        # perché non so a priori da quale nodo parta il percorso più lungo
        for nodo in self._graph.nodes:
            # Il cammino parziale parte dal singolo nodo corrente
            parziale = [nodo]

            # Provo ad allungare ricorsivamente questo cammino
            best_path = self._ricorsioneCammino(parziale, best_path)

        # Restituisco il cammino migliore trovato
        return best_path

    def _ricorsioneCammino(self, parziale, best_path):
        """
        Funzione ricorsiva vera e propria.

        parziale:
        cammino che sto costruendo in questo momento.

        best_path:
        miglior cammino trovato finora.
        """

        # Prendo l'ultimo attore inserito nel cammino parziale
        # Da questo attore cercherò di andare verso un vicino più giovane
        ultimo = parziale[-1]

        # Se il cammino parziale attuale è più lungo del migliore trovato finora,
        # aggiorno il migliore
        if len(parziale) > len(best_path):
            # Faccio una copia della lista
            # perché parziale verrà modificato dai successivi append/pop
            best_path = list(parziale)

        # Analizzo tutti gli attori vicini dell'ultimo nodo
        # Il grafo è NON orientato, quindi uso neighbors()
        for vicino in self._graph.neighbors(ultimo):

            # Condizione 1:
            # il cammino deve essere semplice, quindi non posso ripassare
            # da un attore già presente nel cammino
            if vicino not in parziale:

                # Condizione 2:
                # l'età deve essere strettamente decrescente
                # quindi il vicino deve essere più giovane dell'ultimo attore
                if vicino.eta < ultimo.eta:
                    # Aggiungo il vicino al cammino parziale
                    parziale.append(vicino)

                    # Continuo la ricerca partendo dal nuovo ultimo nodo
                    best_path = self._ricorsioneCammino(parziale, best_path)

                    # Backtracking:
                    # tolgo il vicino appena aggiunto per provare altri percorsi
                    parziale.pop()

        # Restituisco il miglior cammino trovato
        return best_path