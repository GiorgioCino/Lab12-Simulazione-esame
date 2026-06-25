import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        voti = self._model.get_all_voti()

        self._view._ddrating1.options.clear()
        self._view._ddrating2.options.clear()

        for voto in voti:
            self._view._ddrating1.options.append(
                ft.dropdown.Option(str(voto))
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(str(voto))
            )

        self._view._ddrating1.value = None
        self._view._ddrating2.value = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        voto_iniziale = self._view._ddrating1.value
        voto_finale = self._view._ddrating2.value

        if voto_iniziale is None:
            self._view.create_alert("Seleziona voto iniziale.")
            return

        if voto_finale is None:
            self._view.create_alert("Seleziona voto finale.")
            return

        if voto_iniziale > voto_finale:
            self._view.create_alert("voto di inizio deve essere minore al voto di fine.")
            return

        n_nodi, n_archi = self._model.build_graph(voto_iniziale, voto_finale)
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato.")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Voto inizio: {voto_iniziale}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Voto fine: {voto_finale}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {n_archi}")
        )

        archis = self._model.get_edges_info()


        if len(archis) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun arco trovato. Crea prima il grafo.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text("Dettagli degli archi:")
        )

        for a1, a2, peso in archis:
            self._view.txt_result.controls.append(
                ft.Text(f"{a1} - {a2}: {peso} ")
            )

        sizeCompConn = self._model.getInfoCompConnessa()

        self._view.txt_result.controls.append(
            ft.Text(f"componente connessa è composta di {sizeCompConn} nodi"))

        compMaggiore = self._model.getComponenteMaggiore()

        self._view.txt_result.controls.append(
            ft.Text("Componente connessa di dimensione maggiore:")
        )

        for nodo in compMaggiore:
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo} ")
            )

        self._view.update_page()

        self._view.update_page()

    def handleCammino(self, e):
        """
        Metodo collegato al pulsante 'Cerca percorso'.

        Chiede al Model il cammino semplice più lungo con età decrescente
        e lo stampa nella View.
        """

        # Pulisco l'area dei risultati
        self._view.txt_result.controls.clear()

        # Prima controllo che il grafo sia stato creato
        # Se l'utente non ha ancora premuto "Crea grafo",
        # non posso cercare nessun percorso
        if not self._model.grafoCreato():
            self._view.create_alert("Crea prima il grafo.")
            return

        # Chiedo al Model di cercare il cammino massimo
        cammino = self._model.getCamminoMassimo()

        # Se per qualche motivo il cammino è vuoto, stampo un messaggio
        if len(cammino) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato.")
            )

            self._view.update_page()
            return

        # Stampo la lunghezza del cammino
        # Se ho N nodi, il numero di archi è N - 1
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino massimo trovato: {len(cammino)} nodi, {len(cammino) - 1} archi")
        )

        self._view.txt_result.controls.append(
            ft.Text("Attori nel cammino:")
        )

        # Stampo uno per uno gli attori del cammino
        for attore in cammino:
            self._view.txt_result.controls.append(
                ft.Text(f"{attore.name} - età: {attore.eta}")
            )

        # Aggiorno la pagina
        self._view.update_page()