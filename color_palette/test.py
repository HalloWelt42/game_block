from material_colors import MaterialDesign

color = MaterialDesign.Green.M800
print(color.value)

next_color = MaterialDesign.get_neighbors(color,MaterialDesign.Neighbor.NEXT)
print(next_color)

transparent = MaterialDesign.opacity(next_color, 100)
print(transparent)

color = (46, 125, 50, 123)
print(
    MaterialDesign.get(color)
)