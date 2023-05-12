class Chromosome:
    def __init__(self,
                index : int = 0 ,
                value : float = 0.0, 
                binary: str = "",
                fitness: float = 0,
                probabilitaty: float = 0
                ) -> None:
        
        self.index = index
        self.value = value
        self.binary = binary
        self.fitness = fitness
        self.probability = probabilitaty

    
    def __str__(self) -> str:
        return f"\t{self.index:4}: {self.binary} x= {self.value:<20} f(x)= {self.fitness}"
