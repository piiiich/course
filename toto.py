'''
    def destination_test(self, circuit, init_pos, init_speed):
        # teste les différentes positions possibles depuis init_pos avec init_speed
        max_dist = 0
        # liste_coups = [] 
        for point in self.range:

            test_speed = tuple(init_speed[i] + point[i] for i in [0, 1])
            test_dest = tuple(init_pos[i] + test_speed[i] for i in [0, 1])

            further = (dist(self.position(), test_dest) > max_dist)
            in_circuit = (not X.x_tracklimit(self, test_dest, init_pos, circuit))
            towards_end = (X.direction_test(self, test_dest, init_pos, circuit))

            if in_circuit and towards_end and further :
                max_dist = dist(self.position(), test_dest)
                self.speed = test_speed
                dest = test_dest 
                # dest.append(test_dest) 
        # sort 

        return dest'''

# Tri bubble
'''
    def tri_liste_distances(self, init_pos, init_speed):
        # Cette fonction renvoie une liste de tuples (point_destination_(x,y), vitesse)
        liste_distances = self.liste_distances(init_pos, init_speed)
        n = len(liste_distances)
        
        # Tri bubble pour trier les points possibles par distance à l'origine décroissante
        for i in range(n):
            for j in range(0, n-i-1):
                if liste_distances[j][1] < liste_distances[j+1][1]:
                    liste_distances[j], liste_distances[j+1] = liste_distances[j+1], liste_distances[j]

        return [tab[:3] for tab in liste_distances] 
    ''' 


# Tri fusion 
'''
def merge(left, right):
        merged = []
        left_index = 0
        right_index = 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index][1] >= right[right_index][1]:  # Notez l'inversion du signe pour un tri décroissant
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        merged.extend(left[left_index:])
        merged.extend(right[right_index:])

        return merged

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))


        # liste_distances = self.liste_distances(init_pos, init_speed)
        # Tri par fusion pour trier les points possibles par distance à l'origine décroissante
        #liste_coups_triee = merge_sort(liste_coups) 
        #print(f'liste_distances = {[tab[:3] for tab in liste_distances]}')
        #return [tab[:3] for tab in liste_distances]
'''