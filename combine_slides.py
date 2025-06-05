# Combinador de slides para gerar o arquivo index.html completo
import os

HTML_HEADER = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apresentação Reforma Tributária</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@latest/dist/full.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'fh-navy': '#1e3243',
                        'fh-green': '#8bc53f',
                        'fh-lightgray': '#d2d5d0',
                        'fh-mediumgray': '#6d7681'
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background-color: #f9f9f9; }
        .slide { padding: 40px; border-bottom: 1px solid #ccc; background-color: #fff; }
    </style>
</head>
<body>
'''

HTML_FOOTER = '''
<script src="js/scripts.js"></script>
</body>
</html>'''

def combine_slides():
    slide_files = ['slide1.html', 'slide2.html', 'slide3.html', 'slide4.html', 'slide5.html', 'slide6.html', 'slide7.html']

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_HEADER)
        for slide_file in slide_files:
            if os.path.exists(slide_file):
                with open(slide_file, 'r', encoding='utf-8') as slide:
                    f.write(slide.read())
        f.write(HTML_FOOTER)

    print("Slides combinados com sucesso no index.html")

if __name__ == '__main__':
    combine_slides()
