import vtk
import trimesh

def main():
    file_paths = ["object.obj"]  # Example list of file paths

    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)

    # Create render window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 600)

    # Create render window interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    for file_path in file_paths:
        # Read OBJ file
        reader = vtk.vtkOBJReader()
        reader.SetFileName(file_path)

        # Create mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Add actor to renderer
        renderer.AddActor(actor)

        # Calculate dimensions and volume
        dimensions, volume = calculate_dimensions_and_volume(file_path, 'mm')

        # Display results
        display_results(file_path, dimensions, volume, 'mm')

    # Create named colors
    colors = vtk.vtkNamedColors()

    # Create color options and their corresponding keys
    color_options = ["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta"]
    color_keys = ["r", "g", "b", "y", "c", "m"]

    # Create text actor for color options
    text_actor = vtk.vtkTextActor()
    text_actor.GetTextProperty().SetFontSize(20)
    text_actor.GetTextProperty().SetColor(0, 0, 0)
    text_actor.GetTextProperty().SetJustificationToLeft()
    text_actor.GetTextProperty().SetVerticalJustificationToTop()

    # Set initial text
    text = "Color Options:\n"
    for key, color in zip(color_keys, color_options):
        text += f"{key}: {color}\n"
    text_actor.SetInput(text)

    # Add text actor to renderer
    renderer.AddActor(text_actor)

    # Assign the interaction function to a keyboard press event
    renderWindowInteractor.AddObserver("KeyPressEvent", lambda obj, event: change_color(obj, event, actor, colors, color_keys, color_options, renderWindow))

    # Start rendering
    renderWindow.Render()
    renderWindowInteractor.Start()

def change_color(obj, event, actor, colors, color_keys, color_options, renderWindow):
    key = obj.GetKeySym()
    if key in color_keys:
        selected_color = colors.GetColor3d(color_options[color_keys.index(key)])
        actor.GetProperty().SetColor(selected_color)
        renderWindow.Render()

def calculate_dimensions_and_volume(file_path, dimension_unit):
    mesh = trimesh.load_mesh(file_path)

    # Calculate bounding box dimensions
    min_bound, max_bound = mesh.bounds
    dimensions = max_bound - min_bound

    # Convert dimensions to the selected metric unit
    conversion_factors = {'mm': 0.1, 'inches': 2.54}
    conversion_factor = conversion_factors[dimension_unit]
    dimensions *= conversion_factor

    # Calculate volume
    volume = mesh.volume

    # Convert volume to the same unit as dimensions
    volume *= conversion_factor ** 3

    # Return dimensions and volume
    return dimensions, volume

def display_results(file_path, dimensions, volume, dimension_unit):
    print(f"Dimensions of the model in '{file_path}' (in {dimension_unit}):")
    print(f"Width: {dimensions[0]:.2f} {dimension_unit}")
    print(f"Height: {dimensions[1]:.2f} {dimension_unit}")
    print(f"Depth: {dimensions[2]:.2f} {dimension_unit}")
    print(f"Volume: {volume:.2f} {dimension_unit}^3")
    print()

if __name__ == '__main__':
    main()
