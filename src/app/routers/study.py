import os

root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")

js_directory = os.path.join(template_folder, "js")
css_directory = os.path.join(template_folder, "css")
pictures_directory = os.path.join(template_folder, "pictures")


print('root dir', root_dir)
print('template_folder ', template_folder)

print('js_directory ', js_directory)
print('css_directory ', css_directory)
print('images_directory ', pictures_directory)