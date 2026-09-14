from robocute.app import App
from crunge.engine.d2.settings_2d import Settings2D

def main(argv: list[str] | None = None) -> int:
    import sys

    if argv is None:
        argv = sys.argv[1:]

    # Placeholder for actual CLI logic
    print("Arguments received:", argv)

    Settings2D().ppu = 1.0  # Set pixels per unit for 2D rendering

    app = App()
    app.run()

    return 0