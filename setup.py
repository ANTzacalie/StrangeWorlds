from cx_Freeze import setup, Executable

setup(
    name="StrangeWorlds",
    version="3.0",
    description="Game build with Pygame and Python",
    executables=[Executable("mainScript.py")],
    options={
        "build_exe": {
            "includes": ["firstLevel", "secondLevel", "thirdLevel", "settings", "gameFinished"],
            "include_files": [
                "image_caracters",
                "image_objects",
                "level[1]",
                "level[2]",
                "level[3]",
                "icon.png",
                "gameInternalDataBase[A].db"
            ]
        }
    }
)
