from GUI import GUI

if __name__ == '__main__':
    app = GUI.App()
    app.after(1000, app.update)
    app.mainloop()
