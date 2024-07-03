class Queue:
    def __init__(self):
        """Initialise une nouvelle instance de la classe Queue."""
        self.items = []

    def is_empty(self):
        """Vérifie si la file est vide. Renvoie True si la file est vide, False sinon."""
        return not bool(self.items)

    def enqueue(self, data):
        """Ajoute un élément au debut de la file."""
        self.items.insert(0, data)

    def dequeue(self):
        """Reshote un élément de la fin de la file. Renvoie None si la file est vide."""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """Renvoie l'élément au début de la file sans le reshoter. Renvoie None si la file est vide."""
        if not self.is_empty():
            return self.items[0]
        return None

    def size(self):
        """Renvoie le nombre d'éléments dans la file."""
        return len(self.items)

    def get_item(self, i=None):
        """Renvoie l'élément à l'indice i. Renvoie None si l'indice est hors limites."""
        if i is None:
            return self.items
        if i >= 0 and i < len(self.items):
            return self.items[i]
        return None
