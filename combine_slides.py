
# Combinador de slides para gerar o arquivo index.html completo
import os

def combine_slides():
    # Lista de arquivos de slide na ordem correta
    slide_files = ['slide1.html', 'slide2.html', 'slide3.html', 'slide4.html', 'slide5.html', 'slide6.html', 'slide7.html']
    
    # Abrir o arquivo index.html existente
    with open('index.html', 'r', encoding='utf-8') as f:
        header = f.read()
    
    # Combinar o cabeçalho com os slides
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(header)
        
        # Adicionar cada slide
        for slide_file in slide_files:
            if os.path.exists(slide_file):
                with open(slide_file, 'r', encoding='utf-8') as slide:
                    f.write(slide.read())
        
        # Adicionar final do HTML
        f.write('''
    <script src="js/scripts.js"></script>
</body>
</html>''')
    
    print("Slides combinados com sucesso!")

if __name__ == "__main__":
    combine_slides()
