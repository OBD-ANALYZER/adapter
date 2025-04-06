import json
import logging
import os
import time
from tkinter import *
from tkinter import ttk, messagebox

from elm_emulator.animation_curve_editor import AnimationCurveEditor
from elm_emulator.car_emulator import Car


class CarEmulatorGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.car = Car()
        self.lock = False
        self.presets = [x for x in os.listdir(
            os.path.curdir) if x.endswith("json")]

    def start(self):
        root = Tk()
        root.title("Engine Control")
        mainframe = ttk.Frame(root, padding="3 3 3 3")
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
        # fill extra space, if window is resized
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # updates only sliders, used for throttle, brake and animation time sliders
        def update_sliders(_):
            if not self.lock:
                throttle_value = throttle_slider.get()
                brake_value = brake_slider.get()
                # pass values in range [0, 1]
                self.car.update(throttle_value / 100, brake_value / 100)
                throttle_label.config(text=f"Throttle\n{throttle_value:.0f} %")
                brake_label.config(text=f"Brake\n{brake_value:.0f} %")
                anim_scale_value = anim_speed_slider.get()
                anim_speed_label.config(
                    text=f"Animation Speed Multiplier: {anim_scale_value:.1f}x")

        throttle_slider = ttk.Scale(
            mainframe, from_=100, to=0, orient="vertical", command=update_sliders)
        throttle_slider.grid(column=1, columnspan=1, row=0,
                             rowspan=1, padx=2, pady=2, sticky=(W, N, S))
        throttle_label = ttk.Label(mainframe, text="Throttle\n0 %")
        throttle_label.grid(column=0, columnspan=1, row=0,
                            rowspan=1, padx=2, pady=2, sticky=(E, N, S))

        brake_slider = ttk.Scale(
            mainframe, from_=100, to=0, orient="vertical", command=update_sliders)
        brake_slider.grid(column=2, columnspan=1, row=0,
                          rowspan=1, padx=2, pady=2, sticky=(E, N, S))
        brake_label = ttk.Label(mainframe, text="Brake\n0 %")
        brake_label.grid(column=3, columnspan=1, row=0,
                         rowspan=1, padx=2, pady=2, sticky=(W, N, S))

        rpm_label = ttk.Label(mainframe, text="Current RPM: 0")
        rpm_label.grid(column=0, columnspan=4, row=1,
                       rowspan=1, padx=2, pady=2)
        speed_label = ttk.Label(mainframe, text="Current Speed: 0.0 km/h")
        speed_label.grid(column=0, columnspan=4, row=2,
                         rowspan=1, padx=2, pady=2)
        temp_label = ttk.Label(mainframe, text="Engine Temperature: 0.0 °C")
        temp_label.grid(column=0, columnspan=4, row=3,
                        rowspan=1, padx=2, pady=2)
<<<<<<< HEAD
        fuel_label = ttk.Label(mainframe, text="Fuel Level: 100.0 %")
        fuel_label.grid(column=0, columnspan=4, row=4,
                        rowspan=1, padx=2, pady=2)
=======
        
        #gear label *******
         
        gear_label = ttk.Label(mainframe, text="Gear: 1")  # New label for gear
        gear_label.grid(column=0, columnspan=4, row=4,
                         rowspan=1, padx=2, pady=2)
        gear_position_label = ttk.Label(mainframe, text="Gear Position: N")  # New label for gear position
        gear_position_label.grid(column=0, columnspan=4, row=5,
                                  rowspan=1, padx=2, pady=2)

        #*********
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8

        selected = StringVar()
        presets = Variable(value=self.presets)
        listbox = Listbox(mainframe, listvariable=presets, selectmode='browse')
<<<<<<< HEAD
        listbox.grid(column=1, columnspan=2, row=5, rowspan=4,
=======
        listbox.grid(column=1, columnspan=2, row=6, rowspan=4,
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8
                     padx=2, pady=2, sticky=(N, W, E, S))
        listbox.bind('<<ListboxSelect>>', lambda event: selected.set(
            self.presets[listbox.curselection()[0]]))

        def load_curve():
            try:
                with open(selected.get(), 'r') as file:
                    data = json.load(file)
                    animation_curve_gui.curve.points = [
                        (p['x'], p['y']) for p in data['points']]
                    animation_curve_gui.curve.tangents = {(p['x'], p['y']): (
                        t['x'], t['y']) for p, t in zip(data['points'], data['tangents'])}
                    animation_curve_gui.draw_curve()
            except Exception as e:
                logging.error(f"Invalid file or file content: {e}")

        def save_curve():
            try:
                file_name = file_name_entry.get()
                if not file_name.endswith(".json"):
                    file_name += ".json"
                data = {
                    "points": [{"x": p[0], "y": p[1]} for p in animation_curve_gui.curve.points],
                    "tangents": [{"x": t[0], "y": t[1]} for t in animation_curve_gui.curve.tangents.values()]
                }
                with open(file_name, 'w') as file:
                    json.dump(data, file)
                if file_name not in self.presets:
                    self.presets.append(file_name)
                    presets.set(self.presets)
            except Exception as e:
                logging.error(f"Failed to save data: {e}")

        def remove_curve():
            try:
                selected_index = listbox.curselection()  # Get selected index
                if not selected_index:
                    messagebox.showwarning("Warning", "No file selected!")
                    return

                selected_file = listbox.get(selected_index[0])  # Get filename

                # Confirm deletion
                confirm = messagebox.askyesno(
                    "Confirm Delete", f"Delete '{selected_file}'?")
                if not confirm:
                    return

                # Remove from listbox and delete from disk
                if selected_file in self.presets:
                    self.presets.remove(selected_file)
                    presets.set(self.presets)  # Update listbox

                if os.path.exists(selected_file):
                    os.remove(selected_file)

                messagebox.showinfo(
                    "Success", f"Deleted '{selected_file}' successfully!")
            except Exception as e:
                logging.error(f"Failed to remove file: {e}")
                messagebox.showerror("Error", f"Could not remove file: {e}")

        load_curve_button = ttk.Button(
            mainframe, text="Load Hermite Curve", command=load_curve)
<<<<<<< HEAD
        load_curve_button.grid(column=0, columnspan=1, row=6,
                               rowspan=2, padx=2, pady=2, sticky=(E, N, S))

        file_name_entry = ttk.Entry(mainframe)
        file_name_entry.grid(column=3, columnspan=1, row=6,
                             rowspan=1, padx=2, pady=2, sticky=(W, N, S))
        save_curve_button = ttk.Button(
            mainframe, text="Save Hermite Curve", command=save_curve)
        save_curve_button.grid(column=3, columnspan=1, row=7,
                               rowspan=1, padx=2, pady=2, sticky=(W, N, S))
        remove_button = ttk.Button(
            mainframe, text="remove", command=remove_curve)
        remove_button.grid(column=3, row=8, padx=2, pady=2, sticky=(W, N, S))
=======
        load_curve_button.grid(column=0, columnspan=1, row=7,
                               rowspan=2, padx=2, pady=2, sticky=(E, N, S))

        file_name_entry = ttk.Entry(mainframe)
        file_name_entry.grid(column=3, columnspan=1, row=7,
                             rowspan=1, padx=2, pady=2, sticky=(W, N, S))
        save_curve_button = ttk.Button(
            mainframe, text="Save Hermite Curve", command=save_curve)
        save_curve_button.grid(column=3, columnspan=1, row=8,
                               rowspan=1, padx=2, pady=2, sticky=(W, N, S))
        remove_button = ttk.Button(
            mainframe, text="remove", command=remove_curve)
        remove_button.grid(column=3, row=9, padx=2, pady=2, sticky=(W, N, S))
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8

        def animate_curve():
            if len(animation_curve_gui.curve.points) > 1:
                self.lock = True
                throttle_slider.config(state=DISABLED)
                brake_slider.config(state=DISABLED)
                duration = animation_curve_gui.curve.duration() / anim_speed_slider.get()
                self.start_time = root.after(0, animate, duration, time.time())
            else:
                logging.error("Not enough points to animate the curve")

        def animate(duration, start_time):
            elapsed_time = time.time() - start_time  # in second
            t = min(elapsed_time / (duration / 1000.0), 1.0)
            if len(animation_curve_gui.curve.points) > 1:
                y = animation_curve_gui.curve.evaluate(
                    t * animation_curve_gui.curve.duration())

                self.car.speed = y
                speed_label.config(text=f"Current Speed: {y:.1f} km/h")
                self.emulator.database["speed"] = y
                # Calculate and update the engine temperature based on the speed
                # 70°C at speed 0, increases by 0.1°C per km/h
                self.car.engine_temp = 70 + (self.car.speed * 0.1)
                temp_label.config(
                    text=f"Engine Temperature: {self.car.engine_temp:.1f} °C")
                self.emulator.database["engine_temp"] = self.car.engine_temp
                # Update fuel level
                self.car.fuel_level -= self.car.throttle_position * self.car.fuel_consumption_rate
                if self.car.fuel_level < 0:
                    self.car.fuel_level = 0
                fuel_label.config(
                    text=f"Fuel Level: {self.car.fuel_level:.1f} %")
                self.emulator.database["fuel_level"] = self.car.fuel_level
                if t < 1.0:
                    root.after(10, animate, duration, start_time)
                else:
                    self.lock = False
                    throttle_slider.config(state=NORMAL)
                    brake_slider.config(state=NORMAL)
            else:
                self.lock = False
                throttle_slider.config(state=NORMAL)
                brake_slider.config(state=NORMAL)

        anim_speed_slider = ttk.Scale(
            mainframe, from_=0.1, to=2.0, orient="horizontal", value=1, command=update_sliders)
        anim_speed_slider.grid(column=1, columnspan=2,
<<<<<<< HEAD
                               row=9, padx=2, pady=2, sticky=(W, E))
        anim_speed_label = ttk.Label(
            mainframe, text="Animation Speed Multiplier: 1.0x")
        anim_speed_label.grid(column=0, columnspan=1, row=9,
=======
                               row=10, padx=2, pady=2, sticky=(W, E))
        anim_speed_label = ttk.Label(
            mainframe, text="Animation Speed Multiplier: 1.0x")
        anim_speed_label.grid(column=0, columnspan=1, row=10,
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8
                              padx=2, pady=2, sticky=(E, N, S))

        animate_curve_button = ttk.Button(
            mainframe, text="Animate Hermite Curve", command=animate_curve)
        animate_curve_button.grid(
<<<<<<< HEAD
            column=3, columnspan=1, row=9, padx=2, pady=2, sticky=(W, N, S))

        graphframe = ttk.Frame(mainframe, padding="1 1 1 1")
        graphframe.grid(column=0, columnspan=4, row=10,
=======
            column=3, columnspan=1, row=10, padx=2, pady=2, sticky=(W, N, S))

        graphframe = ttk.Frame(mainframe, padding="1 1 1 1")
        graphframe.grid(column=0, columnspan=4, row=11,
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8
                        padx=2, pady=2, sticky=(N, S, E, W))
        animation_curve_gui = AnimationCurveEditor(graphframe)

        def update_values():  # updates rpm, speed,gear, gear position and engine temperature
            if not self.lock:
                self.car.update(self.car.throttle_position,
                                self.car.brake_position)
                rpm_label.config(text=f"Current RPM: {self.car.rpm:.0f}")
                self.emulator.database["rpm"] = self.car.rpm
                speed_label.config(
                    text=f"Current Speed: {self.car.speed:.1f} km/h")
                self.emulator.database["speed"] = self.car.speed
                temp_label.config(
                    text=f"Engine Temperature: {self.car.engine_temp:.1f} °C")
                self.emulator.database["engine_temp"] = self.car.engine_temp
<<<<<<< HEAD
                # Update fuel level
                fuel_label.config(
                    text=f"Fuel Level: {self.car.fuel_level:.1f} %")
                self.emulator.database["fuel_level"] = self.car.fuel_level
=======
                
                #Gear*****************************

                gear_label.config(text=f"Gear: {self.car.gear}")  # Update gear label
                gear_position_label.config(text=f"Gear Position: {self.car.gear_position}")  # Update gear position label
>>>>>>> 35f0e1733d01354de8fd8bdb78ce9f470530d1d8

            root.after(10, update_values)

        # fill extra space, if window is resized
        mainframe.columnconfigure([0, 1, 2, 3], weight=1)
        # fill extra space, if window is resized
        mainframe.rowconfigure([0, 5, 6, 7, 8, 10], weight=1)

        update_values()
        root.mainloop()
