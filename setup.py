import setuptools
from importlib import import_module

def get_dependencies(env_yaml_file):
    import yaml
    with open(env_yaml_file, "r") as f:
        environment = yaml.safe_load(f)
    dependencies = []
    for dep in environment["dependencies"]:
        if not dep.startswith("python"):
            dependencies.append(dep)
    return dependencies

setuptools.setup(
    name="ultimate_plotter",
    author="Massimiliano Galli",
    author_email="massimiliano.galli.95@gmail.com",
    description="HEP data processor and plotter with interfaces to multiple scikit-hep packages",
    packages=["ultimate_plotter"],
    install_requires=get_dependencies("ultimate_plotter_env.yml"),
    scripts = ["scripts/basic_plot.py", "scripts/stack_plot.py"]
)
