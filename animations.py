def spring_animation(list, interval, index, counter, increase):
    """Crea una animación de ida y vuelta a intervalos iguales 
    y devuelve un índice, contador e incremento"""

    counter +=1

    if index >= len(list) - 1:
        index = len(list) - 1


    if counter >= interval:

        if index == len(list) - 1:
            increase = -1

        if index <= 0:
            index = 0
            increase = 1
        
        index += increase
        counter = 0

    return index, counter, increase

def linear_animation(list, interval, index, counter, increase=1):
    """Crea una animación lineal en bucle infinito, devuelve índice y contador"""
    counter +=1
    
    if index >= len(list) - 1:
        index = len(list) - 1


    if counter >= interval:

        if index < len(list) - 1:
            index += increase

        else:
            index = 0
        
        counter = 0

    return index, counter
