if __name__ == "__main__":

    from PIL import Image
    import os.path
    image = Image.open(os.path.join(os.path.dirname(__file__), "assets/cover.png"))
    image.show()

    from biostats import app
    root = app.App()
    root.mainloop()
    