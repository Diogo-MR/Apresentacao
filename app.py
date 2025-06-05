# app.py
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Timer

# Criar diretórios necessários
os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)

# Criar arquivo CSS
with open('css/styles.css', 'w', encoding='utf-8') as f:
    f.write("""
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: white;
}
.slide {
    display: none;
    height: 100vh;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    overflow: hidden;
}
.active {
    display: block;
}
.animate-in {
    animation: fadeIn 0.8s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.card-scenario {
    transition: all 0.3s ease;
}
.card-scenario:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
.progress-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    height: 5px;
    background-color: #8bc53f;
    z-index: 100;
}
.nav-dots {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 100;
}
.nav-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #d2d5d0;
    cursor: pointer;
    transition: all 0.3s ease;
}
.nav-dot.active {
    background-color: #8bc53f;
    transform: scale(1.2);
}
.chart-container {
    position: relative;
    margin: auto;
    height: 300px;
    width: 100%;
}
.arrow-animation {
    animation: bounce 2s infinite;
}
@keyframes bounce {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(15px); }
}
""")

# Criar arquivo JavaScript
with open('js/scripts.js', 'w', encoding='utf-8') as f:
    f.write("""
// Gerenciamento de slides
let currentSlide = 1;
const totalSlides = document.querySelectorAll('.slide').length;

function updateSlide() {
    document.querySelectorAll('.slide').forEach((slide, index) => {
        slide.classList.remove('active');
        if (index + 1 === currentSlide) {
            slide.classList.add('active');
        }
    });
    
    document.querySelectorAll('.nav-dot').forEach((dot, index) => {
        dot.classList.remove('active');
        if (index + 1 === currentSlide) {
            dot.classList.add('active');
        }
    });
    
    // Atualiza a barra de progresso
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = `${(currentSlide / totalSlides) * 100}%`;
}

function nextSlide() {
    if (currentSlide < totalSlides) {
        currentSlide++;
        updateSlide();
    }
}

function prevSlide() {
    if (currentSlide > 1) {
        currentSlide--;
        updateSlide();
    }
}

document.getElementById('nextBtn').addEventListener('click', nextSlide);
document.getElementById('prevBtn').addEventListener('click', prevSlide);

// Criar pontos de navegação
const navDots = document.getElementById('navDots');
for (let i = 1; i <= totalSlides; i++) {
    const dot = document.createElement('div');
    dot.classList.add('nav-dot');
    if (i === 1) dot.classList.add('active');
    dot.addEventListener('click', () => {
        currentSlide = i;
        updateSlide();
    });
    navDots.appendChild(dot);
}

// Navegação por teclado
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
        nextSlide();
    } else if (e.key === 'ArrowLeft') {
        prevSlide();
    }
});

// Gráfico de Impacto
const ctx = document.getElementById('impactChart').getContext('2d');
const impactChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Carga Tributária', 'Aproveitamento de Créditos (%)', 'Risco de Autuações', 'Adaptação Operacional', 'Posição Competitiva'],
        datasets: [
            {
                label: 'Sem Consultoria',
                data: [20, 60, 90, 80, 30],
                backgroundColor: 'rgba(239, 68, 68, 0.7)',
                borderColor: 'rgba(239, 68, 68, 1)',
                borderWidth: 1
            },
            {
                label: 'Com FH Souza Advogados',
                data: [-10, 95, 10, 20, 90],
                backgroundColor: 'rgba(139, 197, 63, 0.7)',
                borderColor: 'rgba(139, 197, 63, 1)',
                borderWidth: 1
            },
            {
                label: 'Sem Ação Específica',
                data: [8, 75, 50, 60, 50],
                backgroundColor: 'rgba(234, 179, 8, 0.7)',
                borderColor: 'rgba(234, 179, 8, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Impacto (%)'
                }
            }
        },
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.dataIndex === 0) { // Carga Tributária
                            return label + context.raw + '%';
                        } else if (context.dataIndex === 1) { // Aproveitamento
                            return label + context.raw + '%';
                        } else if (context.dataIndex === 2) { // Risco
                            return label + (context.raw > 70 ? 'Alto' : context.raw > 30 ? 'Médio' : 'Baixo');
                        } else if (context.dataIndex === 3) { // Adaptação
                            return label + (context.raw > 70 ? 'Difícil' : context.raw > 30 ? 'Moderada' : 'Fácil');
                        } else { // Posição
                            return label + (context.raw > 70 ? 'Forte' : context.raw > 30 ? 'Neutra' : 'Fraca');
                        }
                    }
                }
            }
        }
    }
});
""")

# Criar arquivo HTML com o conteúdo da apresentação
with open('index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impactos da Reforma Tributária - FH Souza Advogados</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@latest"></script>
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
    <link href="css/styles.css" rel="stylesheet">
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    
    <!-- Controles de navegação -->
    <div class="fixed top-1/2 left-4 transform -translate-y-1/2 z-50">
        <button id="prevBtn" class="bg-fh-navy text-white p-2 rounded-full opacity-70 hover:opacity-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
        </button>
    </div>
    <div class="fixed top-1/2 right-4 transform -translate-y-1/2 z-50">
        <button id="nextBtn" class="bg-fh-navy text-white p-2 rounded-full opacity-70 hover:opacity-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
        </button>
    </div>
    
    <div class="nav-dots" id="navDots"></div>
    <!-- SLIDE 1: Capa -->
    <div class="slide active bg-white" id="slide1">
        <div class="flex flex-col items-center justify-center h-full p-10">
            <div class="flex items-center mb-10 animate-in">
                <div class="bg-fh-navy p-4 rounded-lg">
                    <span class="text-fh-green text-5xl font-bold">FH</span>
                </div>
                <div class="ml-4">
                    <span class="text-fh-green text-5xl font-bold">SOUZA.</span>
                    <span class="block text-fh-navy text-xl tracking-widest">ADVOGADOS</span>
                </div>
            </div>
            <h1 class="text-5xl font-bold text-fh-navy mb-4 text-center animate-in" style="animation-delay: 0.3s">Reforma Tributária</h1>
            <h2 class="text-3xl font-semibold text-fh-mediumgray mb-12 text-center animate-in" style="animation-delay: 0.6s">Impactos para Concessionárias e Indústria Automotiva</h2>
            
            <div class="flex items-center justify-center animate-in" style="animation-delay: 0.9s">
                <svg class="w-64 h-64" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#d2d5d0" stroke-width="8" />
                    <path d="M50 10 A40 40 0 0 1 90 50" stroke="#8bc53f" stroke-width="8" fill="none" />
                    <path d="M90 50 A40 40 0 0 1 70 85" stroke="#6d7681" stroke-width="8" fill="none" />
                    <path d="M70 85 A40 40 0 0 1 30 85" stroke="#1e3243" stroke-width="8" fill="none" />
                    <path d="M30 85 A40 40 0 0 1 10 50" stroke="#d2d5d0" stroke-width="8" fill="none" />
                </svg>
            </div>
            
            <p class="text-xl text-fh-navy mt-10 animate-in" style="animation-delay: 1.2s">Lei Complementar nº 214, de 16 de janeiro de 2025</p>
        </div>
    </div>
    <!-- SLIDE 2: Introdução à Reforma -->
    <div class="slide bg-white" id="slide2">
        <div class="h-full flex flex-col">
            <header class="bg-fh-navy p-4">
                <div class="flex items-center">
                    <div class="bg-fh-navy p-2 rounded-lg">
                        <span class="text-fh-green text-2xl font-bold">FH</span>
                    </div>
                    <h2 class="text-white text-xl ml-4">O Novo Sistema Tributário Brasileiro</h2>
                </div>
            </header>
            
            <div class="flex-grow p-10 flex flex-col items-center justify-center">
                <h3 class="text-3xl font-bold text-fh-navy mb-10 text-center">O que muda com a Reforma Tributária?</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl">
                    <div class="bg-white shadow-lg rounded-lg p-6 border-t-4 border-fh-green">
                        <h4 class="text-xl font-bold text-fh-navy mb-3">Simplificação</h4>
                        <p class="text-fh-mediumgray">Substituição de diversos tributos (PIS, COFINS, IPI, ICMS, ISS) por apenas três: IBS, CBS e IS.</p>
                    </div>
                    
                    <div class="bg-white shadow-lg rounded-lg p-6 border-t-4 border-fh-navy">
                        <h4 class="text-xl font-bold text-fh-navy mb-3">Não-cumulatividade</h4>
                        <p class="text-fh-mediumgray">Sistema de créditos amplo, com possibilidade de aproveitamento em toda a cadeia produtiva.</p>
                    </div>
                    
                    <div class="bg-white shadow-lg rounded-lg p-6 border-t-4 border-fh-lightgray">
                        <h4 class="text-xl font-bold text-fh-navy mb-3">Transição</h4>
                        <p class="text-fh-mediumgray">Implementação gradual ao longo de vários anos, exigindo adaptação progressiva das empresas.</p>
                    </div>
                </div>
                
                <div class="mt-12 w-full max-w-6xl">
                    <div class="bg-fh-lightgray/20 p-6 rounded-lg border-l-4 border-fh-green">
                        <p class="text-fh-navy text-lg">
                            <span class="font-bold">Atenção:</span> Para o setor automotivo, as mudanças são especialmente significativas, impactando toda a cadeia de fornecimento, desde a fabricação até a venda ao consumidor final.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- SLIDE 3: Três Cenários -->
    <div class="slide bg-white" id="slide3">
        <div class="h-full flex flex-col">
            <header class="bg-fh-navy p-4">
                <div class="flex items-center">
                    <div class="bg-fh-navy p-2 rounded-lg">
                        <span class="text-fh-green text-2xl font-bold">FH</span>
                    </div>
                    <h2 class="text-white text-xl ml-4">Cenários de Impacto</h2>
                </div>
            </header>
            
            <div class="flex-grow p-10">
                <h3 class="text-3xl font-bold text-fh-navy mb-10 text-center">Três Cenários Possíveis</h3>
                
                <div class="flex flex-col md:flex-row gap-6 h-[70vh]">
                    <!-- Cenário 1 -->
                    <div class="card-scenario flex-1 bg-gradient-to-b from-red-50 to-red-100 rounded-xl shadow-lg overflow-hidden">
                        <div class="bg-red-500 text-white font-bold py-4 px-6 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <h4 class="text-xl">Pior Cenário</h4>
                        </div>
                        <div class="p-6 overflow-auto h-[calc(100%-64px)]">
                            <p class="font-bold text-red-600 mb-4">Sem consultoria especializada</p>
                            <ul class="space-y-3">
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Aumento inesperado da carga tributária em até 15-20%</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Perda significativa de créditos tributários no período de transição</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Exposição a multas e penalidades por erros de cálculo (até 75% do valor devido)</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Paralisação parcial das operações por incompatibilidade dos sistemas</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Conflitos com fornecedores e clientes sobre responsabilidade tributária</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Decisões equivocadas de investimento em sistemas inadequados</span>
                                </li>
                                <li class="flex items-start">
                                    <svg class="h-6 w-6 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                    <span>Perda de competitividade no mercado</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    
                    <!-- Continuação do HTML com os outros slides... -->
                    <!-- (O HTML completo foi cortado para manter a resposta dentro do limite) -->
                </div>
            </div>
        </div>
    </div>
    <!-- Restante dos slides... -->
    <script src="js/scripts.js"></script>
</body>
</html>""")

# Classe personalizada do manipulador HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

def open_browser():
    webbrowser.open('http://localhost:8000')

# Função principal
def main():
    print("Iniciando Apresentação da Reforma Tributária...")
    print("Iniciando servidor web...")
    server = HTTPServer(('localhost', 8000), MyHandler)
    print("Abrindo navegador...")
    Timer(1, open_browser).start()
    try:
        print("Servidor rodando em http://localhost:8000")
        print("Pressione Ctrl+C para fechar o servidor")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDesligando servidor...")
        server.shutdown()

if __name__ == "__main__":
    main()
