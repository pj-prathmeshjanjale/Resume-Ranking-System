with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('        if app_theme == "☀️ Light Mode":', '    if app_theme == "☀️ Light Mode":')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed indentation")
