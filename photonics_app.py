from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import photonics

# GUI Application
class OpticalSystemApp(App):
    def build(self):
        self.optical_system = photonics.OpticalSystem()
        self.main_layout = BoxLayout(orientation='vertical')

        # Add buttons for each optical component
        button_layout = GridLayout(cols = 3, size_hint_y = None)
        button_layout.bind(minimum_height = button_layout.setter('height'))

        add_free_space_button = Button(text = 'Add Free Space')
        add_free_space_button.bind(on_press = self.add_free_space)
        button_layout.add_widget(add_free_space_button)

        add_thin_lens_button = Button(text = 'Add Thin Lens')
        add_thin_lens_button.bind(on_press = self.add_thin_lens)
        button_layout.add_widget(add_thin_lens_button)

        add_planar_boundary_button = Button(text = 'Add Planar Boundary')
        add_planar_boundary_button.bind(on_press = self.add_planar_boundary)
        button_layout.add_widget(add_planar_boundary_button)

        add_spherical_boundary_button = Button(text = 'Add Spherical Boundary')
        add_spherical_boundary_button.bind(on_press = self.add_spherical_boundary)
        button_layout.add_widget(add_spherical_boundary_button)

        add_planar_mirror_button = Button(text = 'Add Planar Mirror')
        add_planar_mirror_button.bind(on_press = self.add_planar_mirror)
        button_layout.add_widget(add_planar_mirror_button)

        add_spherical_mirror_button = Button(text = 'Add Spherical Mirror')
        add_spherical_mirror_button.bind(on_press = self.add_spherical_mirror)
        button_layout.add_widget(add_spherical_mirror_button)

        add_thick_lens_button = Button(text = 'Add Thick Lens')
        add_thick_lens_button.bind(on_press = self.add_thick_lens)
        button_layout.add_widget(add_thick_lens_button)

        self.main_layout.add_widget(button_layout)

        # Add fields for beam parameters
        beam_layout = BoxLayout(orientation = 'horizontal')

        self.height_input = TextInput(hint_text = 'Beam Height', input_filter = 'float')
        beam_layout.add_widget(self.height_input)

        self.angle_input = TextInput(hint_text = 'Beam Angle', input_filter = 'float')
        beam_layout.add_widget(self.angle_input)

        self.main_layout.add_widget(beam_layout)

        # Add propagate button
        propagate_button = Button(text = 'Propagate Beam')
        propagate_button.bind(on_press = self.propagate_beam)
        self.main_layout.add_widget(propagate_button)

        # Add clear system button
        clear_button = Button(text = 'Clear System')
        clear_button.bind(on_press = self.clear_system)
        self.main_layout.add_widget(clear_button)

        # Add label to display the current optical system
        self.system_label = Label(text = str(self.optical_system))
        self.main_layout.add_widget(self.system_label)

        return self.main_layout
    
    def add_free_space(self, instance):
        # Prompt user to enter the distance
        content = BoxLayout(orientation = 'vertical')
        distance_input = TextInput(hint_text = 'Distance', input_filter = 'float')
        content.add_widget(distance_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)
        popup = Popup(title = 'Add Free Space', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_free_space(distance_input.text, popup))
        popup.open()

    def confirm_add_free_space(self, distance, popup):
        try:
            distance = float(distance)
            self.optical_system.add(photonics.FreeSpace(distance = distance))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_thin_lens(self, instance):
        # Prompt user to enter the focal length
        content = BoxLayout(orientation = 'vertical')
        focal_length_input = TextInput(hint_text = 'Focal Length', input_filter = 'float')
        content.add_widget(focal_length_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)
        popup = Popup(title = 'Add Thin Lens', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_thin_lens(focal_length_input.text, popup))
        popup.open()

    def confirm_add_thin_lens(self, focal_length, popup):
        try:
            focal_length = float(focal_length)
            self.optical_system.add(photonics.ThinLens(focal_length = focal_length))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_planar_boundary(self, instance):
        # Prompt user to enter n1 and n2
        content = BoxLayout(orientation = 'vertical')
        n1_input = TextInput(hint_text = 'n1', input_filter = 'float')
        content.add_widget(n1_input)
        n2_input = TextInput(hint_text = 'n2', input_filter = 'float')
        content.add_widget(n2_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)

        popup = Popup(title = 'Add Planar Boundary', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_planar_boundary(n1_input.text, n2_input.text, popup))
        popup.open()

    def confirm_add_planar_boundary(self, n1, n2, popup):
        try:
            n1 = float(n1)
            n2 = float(n2)
            self.optical_system.add(photonics.PlanarBoundary(n1 = n1, n2 = n2))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_spherical_boundary(self, instance):
        # prompt user to input radius, n1, and n2
        content = BoxLayout(orientation = 'vertical')
        radius_input = TextInput(hint_text = 'Radius', input_filter = 'float')
        content.add_widget(radius_input)
        n1_input = TextInput(hint_text = 'n1', input_filter = 'float')
        content.add_widget(n1_input)
        n2_input = TextInput(hint_text = 'n2', input_filter = 'float')
        content.add_widget(n2_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)

        popup = Popup(title = 'Add Spherical Boundary', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_spherical_boundary(radius_input.text, n1_input.text, n2_input.text, popup))
        popup.open()

    def confirm_add_spherical_boundary(self, radius, n1, n2, popup):
        try:
            radius = float(radius)
            n1 = float(n1)
            n2 = float(n2)
            self.optical_system.add(photonics.SphericalBoundary(radius = radius, n1 = n1, n2 = n2))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_planar_mirror(self, instance):
        content = BoxLayout(orientation = 'vertical')
        add_button = Button(text = 'Add')
        content.add_widget(add_button)

        popup = Popup(title = 'Add Planar Mirror', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_planar_mirror(popup))
        popup.open()

    def confirm_add_planar_mirror(self, popup):
        try:
            self.optical_system.add(photonics.PlanarMirror())
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_spherical_mirror(self, instance):
        content = BoxLayout(orientation = 'vertical')
        radius_input = TextInput(hint_text = 'Radius', input_filter = 'float')
        content.add_widget(radius_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)

        popup = Popup(title = 'Add Spherical Mirror', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_spherical_mirror(radius_input.text, popup))
        popup.open()

    def confirm_add_spherical_mirror(self, radius, popup):
        try:
            radius = float(radius)
            self.optical_system.add(photonics.SphericalMirror(radius = radius))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))

    def add_thick_lens(self, instance):
        content = BoxLayout(orientation = 'vertical')
        r1_input = TextInput(hint_text = 'R1', input_filter = 'float')
        content.add_widget(r1_input)
        r2_input = TextInput(hint_text = 'R2', input_filter = 'float')
        content.add_widget(r2_input)
        width_input = TextInput(hint_text = 'Width', input_filter = 'float')
        content.add_widget(width_input)
        n1_input = TextInput(hint_text = 'n1', input_filter = 'float')
        content.add_widget(n1_input)
        n2_input = TextInput(hint_text = 'n2', input_filter = 'float')
        content.add_widget(n2_input)
        add_button = Button(text = 'Add')
        content.add_widget(add_button)

        popup = Popup(title = 'Add Thick Lens', content = content, size_hint = (0.5, 0.5))
        add_button.bind(on_press = lambda x: self.confirm_add_thick_lens(r1_input.text, r2_input.text, width_input.text, n1_input.text, n2_input.text, popup))
        popup.open()

    def confirm_add_thick_lens(self, r1, r2, width, n1, n2, popup):
        try:
            r1 = float(r1)
            r2 = float(r2)
            width = float(width)
            n1 = float(n1)
            n2 = float(n2)
            self.optical_system.add(photonics.ThickLens(r1 = r1, r2 = r2, width = width, n1 = n1, n2 = n2))
            self.system_label.text = str(self.optical_system)
            popup.dismiss()
        except ValueError:
            popup.content.add_widget(Label(text = 'Invalid input!'))


    def propagate_beam(self, instance):
        try:
            height = float(self.height_input.text)
            angle = float(self.angle_input.text)
            beam = photonics.Beam(height, angle)
            result = self.optical_system.propagate(beam)
            popup = Popup(title = 'Beam Propagation Result', content = Label(text = f'Height: {result[0, 0]}, Angle: {result[1, 0]}'), size_hint = (0.5, 0.5))
            popup.open()
        except ValueError:
            popup = Popup(title = 'Error', content = Label(text = 'Invalid input for beam parameters!'), size_hint = (0.5, 0.5))
            popup.open()
        except Exception as e:
            popup = Popup(title = 'Error', content = Label(text = str(e)), size_hint = (0.5, 0.5))
            popup.open()

    def clear_system(self, instance):
        self.optical_system.clear()
        self.system_label.text = str(self.optical_system)

if __name__ == '__main__':
    OpticalSystemApp().run()
