from cx_Freeze import setup, Executable

base = None
executables = [Executable("src/main.py")]
#Renseignez ici la liste complète des packages utilisés par votre application
packages = ['idna', 'wx','os']
options = {
    'build_exe': {    
        'packages':packages,
    },
}
#Adaptez les valeurs des variables "name", "version", "description" à votre programme.
setup(
    name = "BlindIDE",
    options = options,
    version = "1.0",
    description = 'Voici mon programme',
    executables = executables
)
