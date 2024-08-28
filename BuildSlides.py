import sys
from jinja2 import Template
from bs4 import BeautifulSoup


if __name__ == "__main__":
    print(sys.argv[1:])
    animation_names = sys.argv[1:]
    animations = {}
    for ani in animation_names:
        with open(f"intermediate_html/{ani}.html") as f:
            ani_soup = BeautifulSoup(f, features="lxml")
            ani_data = ''.join([str(c) for c in ani_soup.find("div", class_="slides").contents])
            animations[ani] = str(ani_data)

    with open("presentation_template.j2", "r") as f:
        template_data = f.read()

    template = Template(template_data)
    html = template.render(animations)

    with open("presentation.html", "w") as f:
        f.write(html)