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

    