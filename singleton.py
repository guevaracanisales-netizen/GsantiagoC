class Arbitro:

    _instancia = None   

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.nombre = "Wilmar Roldán"
            cls._instancia.minuto = 0
            print("Árbitro creado: Wilmar Roldán entra a la cancha")
        return cls._instancia

    def pitar_gol(self, equipo):
        self.minuto += 22
        print(f"Min {self.minuto} Gol de {equipo}")

    def pitar_falta(self, jugador):
        self.minuto += 8
        print(f"Min {self.minuto}  Falta de {jugador}")

    def tarjeta_roja(self, jugador):
        self.minuto += 25
        print(f"Min {self.minuto}  Roja a {jugador}")


arbitro_local     = Arbitro()   
arbitro_visitante = Arbitro()   

print(arbitro_local is arbitro_visitante)   

arbitro_local.pitar_gol("Millonarios")
arbitro_visitante.pitar_falta("Daniel Torres")
arbitro_local.tarjeta_roja("Rodrigo Contreras")
arbitro_visitante.pitar_gol("Santa fe")
