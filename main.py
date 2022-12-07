import controller
print("Launching the space team")

controls = controller.Controls(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

while True:
    print(controls.fv1.state)
