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

document.addEventListener('DOMContentLoaded', function() {
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
    if (document.getElementById('impactChart')) {
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
    }
});
""")

# Criar arquivo HTML principal (index.html) - topo da página
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
""")

# Criar arquivo com os slides - cada slide em um arquivo separado
# Slide 1
with open('slide1.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 1: Capa -->
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
""")

# Slide 2
with open('slide2.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 2: Introdução à Reforma -->
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
""")

# Slide 3
with open('slide3.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 3: Três Cenários -->
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
                
                <!-- Cenário 2 -->
                <div class="card-scenario flex-1 bg-gradient-to-b from-green-50 to-green-100 rounded-xl shadow-lg overflow-hidden">
                    <div class="bg-fh-green text-white font-bold py-4 px-6 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h4 class="text-xl">Melhor Cenário</h4>
                    </div>
                    <div class="p-6 overflow-auto h-[calc(100%-64px)]">
                        <p class="font-bold text-fh-green mb-4">Com consultoria da FH Souza Advogados</p>
                        <ul class="space-y-3">
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Otimização da carga tributária com redução de até 10%</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Aproveitamento integral de créditos (> 95%)</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Segurança fiscal e previsibilidade nos negócios</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Implementação antecipada de sistemas compatíveis</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Processos internos otimizados e alinhados às novas regras</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Vantagem competitiva na precificação durante a transição</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-fh-green mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Estruturação estratégica para minimizar o Imposto Seletivo</span>
                            </li>
                        </ul>
                    </div>
                </div>
                
                <!-- Cenário 3 -->
                <div class="card-scenario flex-1 bg-gradient-to-b from-yellow-50 to-yellow-100 rounded-xl shadow-lg overflow-hidden">
                    <div class="bg-yellow-500 text-white font-bold py-4 px-6 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h4 class="text-xl">Cenário Provável</h4>
                    </div>
                    <div class="p-6 overflow-auto h-[calc(100%-64px)]">
                        <p class="font-bold text-yellow-700 mb-4">Sem ação específica</p>
                        <ul class="space-y-3">
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Aumento moderado da carga tributária (5-8%)</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Aproveitamento parcial de créditos (70-80%)</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Riscos fiscais moderados por erros pontuais</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Adaptação reativa e tardia aos requisitos legais</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Dificuldades transitórias na cadeia comercial</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Posicionamento mercadológico neutro</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="h-6 w-6 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span>Sobrecarga das equipes contábil e fiscal</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""")

# Slides restantes em arquivos separados...
# Slide 4
with open('slide4.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 4: Análise Comparativa -->
<div class="slide bg-white" id="slide4">
    <div class="h-full flex flex-col">
        <header class="bg-fh-navy p-4">
            <div class="flex items-center">
                <div class="bg-fh-navy p-2 rounded-lg">
                    <span class="text-fh-green text-2xl font-bold">FH</span>
                </div>
                <h2 class="text-white text-xl ml-4">Análise Comparativa</h2>
            </div>
        </header>
        
        <div class="flex-grow p-10 flex flex-col items-center">
            <h3 class="text-3xl font-bold text-fh-navy mb-10 text-center">Comparativo dos Cenários</h3>
            
            <div class="w-full max-w-6xl mb-10">
                <div class="chart-container">
                    <canvas id="impactChart"></canvas>
                </div>
            </div>
            
            <div class="w-full max-w-6xl overflow-auto">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-fh-navy text-white">
                            <th class="p-4 text-left">Aspecto</th>
                            <th class="p-4 text-center">Sem Consultoria</th>
                            <th class="p-4 text-center">Com FH Souza</th>
                            <th class="p-4 text-center">Sem Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b border-fh-lightgray">
                            <td class="p-4 font-semibold">Carga Tributária Efetiva</td>
                            <td class="p-4 text-center bg-red-100 text-red-700">+15% a +20%</td>
                            <td class="p-4 text-center bg-green-100 text-green-700">Até -10%</td>
                            <td class="p-4 text-center bg-yellow-100 text-yellow-700">+5% a +8%</td>
                        </tr>
                        <tr class="border-b border-fh-lightgray">
                            <td class="p-4 font-semibold">Aproveitamento de Créditos</td>
                            <td class="p-4 text-center bg-red-100 text-red-700">Baixo (< 60%)</td>
                            <td class="p-4 text-center bg-green-100 text-green-700">Alto (> 95%)</td>
                            <td class="p-4 text-center bg-yellow-100 text-yellow-700">Médio (70-80%)</td>
                        </tr>
                        <tr class="border-b border-fh-lightgray">
                            <td class="p-4 font-semibold">Risco de Autuações</td>
                            <td class="p-4 text-center bg-red-100 text-red-700">Alto</td>
                            <td class="p-4 text-center bg-green-100 text-green-700">Muito Baixo</td>
                            <td class="p-4 text-center bg-yellow-100 text-yellow-700">Moderado</td>
                        </tr>
                        <tr class="border-b border-fh-lightgray">
                            <td class="p-4 font-semibold">Adaptação Operacional</td>
                            <td class="p-4 text-center bg-red-100 text-red-700">Traumática</td>
                            <td class="p-4 text-center bg-green-100 text-green-700">Planejada</td>
                            <td class="p-4 text-center bg-yellow-100 text-yellow-700">Reativa</td>
                        </tr>
                        <tr>
                            <td class="p-4 font-semibold">Posição Competitiva</td>
                            <td class="p-4 text-center bg-red-100 text-red-700">Deteriorada</td>
                            <td class="p-4 text-center bg-green-100 text-green-700">Fortalecida</td>
                            <td class="p-4 text-center bg-yellow-100 text-yellow-700">Neutra</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
""")

# Criar o arquivo Python que combina todos os slides e executa o servidor
with open('combine_slides.py', 'w', encoding='utf-8') as f:
    f.write("""
# Combinador de slides para gerar o arquivo index.html completo
import os

def combine_slides():
    # Lista de arquivos de slide na ordem correta
    slide_files = ['slide1.html', 'slide2.html', 'slide3.html', 'slide4.html']
    
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
""")

# Criar os slides restantes (slides 5, 6 e 7)
with open('slide5.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 5: Benefícios da FH Souza -->
<div class="slide bg-white" id="slide5">
    <div class="h-full flex flex-col">
        <header class="bg-fh-navy p-4">
            <div class="flex items-center">
                <div class="bg-fh-navy p-2 rounded-lg">
                    <span class="text-fh-green text-2xl font-bold">FH</span>
                </div>
                <h2 class="text-white text-xl ml-4">Por que escolher a FH Souza?</h2>
            </div>
        </header>
        
        <div class="flex-grow p-10">
            <div class="flex flex-col md:flex-row h-full">
                <div class="md:w-1/2 flex flex-col justify-center pr-10">
                    <h3 class="text-3xl font-bold text-fh-navy mb-8">Nossa Abordagem 5C</h3>
                    
                    <div class="flex flex-col space-y-6">
                        <div class="flex items-center">
                            <div class="w-14 h-14 rounded-full bg-fh-lightgray flex items-center justify-center">
                                <span class="text-fh-navy font-bold text-xl">1</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-xl font-bold text-fh-navy">CONEXÃO</h4>
                                <p class="text-fh-mediumgray">Coleta dos dados fiscais do cliente.</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="w-14 h-14 rounded-full bg-fh-lightgray flex items-center justify-center">
                                <span class="text-fh-navy font-bold text-xl">2</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-xl font-bold text-fh-navy">COMPREENSÃO</h4>
                                <p class="text-fh-mediumgray">Organização das informações para análise profunda.</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="w-14 h-14 rounded-full bg-fh-green flex items-center justify-center">
                                <span class="text-white font-bold text-xl">3</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-xl font-bold text-fh-green">CONFIGURAÇÃO</h4>
                                <p class="text-fh-mediumgray">Diagnóstico detalhado e personalização de estratégias.</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="w-14 h-14 rounded-full bg-fh-mediumgray flex items-center justify-center">
                                <span class="text-white font-bold text-xl">4</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-xl font-bold text-fh-navy">CORREÇÃO</h4>
                                <p class="text-fh-mediumgray">Implementação das soluções fiscais.</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="w-14 h-14 rounded-full bg-fh-navy flex items-center justify-center">
                                <span class="text-white font-bold text-xl">5</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-xl font-bold text-fh-navy">CONTROLE</h4>
                                <p class="text-fh-mediumgray">Monitoramento contínuo e configurações pelo FH Hub.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="md:w-1/2 flex flex-col justify-center pl-10 mt-10 md:mt-0">
                    <h3 class="text-3xl font-bold text-fh-navy mb-8">Benefícios Exclusivos</h3>
                    
                    <div class="space-y-6">
                        <div class="bg-fh-navy/5 p-6 rounded-lg border-l-4 border-fh-green">
                            <h4 class="text-xl font-bold text-fh-navy mb-2">Expertise Técnica</h4>
                            <p class="text-fh-mediumgray">Nossa equipe conta com especialistas em tributação do setor automotivo, com profundo conhecimento da LC 214/2025.</p>
                        </div>
                        
                        <div class="bg-fh-navy/5 p-6 rounded-lg border-l-4 border-fh-green">
                            <h4 class="text-xl font-bold text-fh-navy mb-2">Tecnologia Proprietária</h4>
                            <p class="text-fh-mediumgray">Utilizamos o FH Hub para simulações, análises de impacto e monitoramento contínuo das obrigações fiscais.</p>
                        </div>
                        
                        <div class="bg-fh-navy/5 p-6 rounded-lg border-l-4 border-fh-green">
                            <h4 class="text-xl font-bold text-fh-navy mb-2">Abordagem Preventiva</h4>
                            <p class="text-fh-mediumgray">Antecipamos problemas e oportunidades antes que impactem seu negócio, com planejamento tributário legítimo.</p>
                        </div>
                        
                        <div class="bg-fh-navy/5 p-6 rounded-lg border-l-4 border-fh-green">
                            <h4 class="text-xl font-bold text-fh-navy mb-2">Suporte Contínuo</h4>
                            <p class="text-fh-mediumgray">Acompanhamento durante todo o período de transição e implementação das mudanças tributárias.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""")

with open('slide6.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 6: Call to Action -->
<div class="slide bg-white" id="slide6">
    <div class="h-full flex flex-col">
        <header class="bg-fh-navy p-4">
            <div class="flex items-center">
                <div class="bg-fh-navy p-2 rounded-lg">
                    <span class="text-fh-green text-2xl font-bold">FH</span>
                </div>
                <h2 class="text-white text-xl ml-4">Próximos Passos</h2>
            </div>
        </header>
        
        <div class="flex-grow flex flex-col justify-center items-center p-10 text-center">
            <h3 class="text-4xl font-bold text-fh-navy mb-8">Prepare-se para a Reforma Tributária</h3>
            
            <div class="w-full max-w-4xl flex flex-col md:flex-row gap-8 mb-12">
                <div class="flex-1 bg-fh-navy/5 p-8 rounded-lg border-t-4 border-fh-green">
                    <div class="mb-4">
                        <span class="inline-block w-16 h-16 rounded-full bg-fh-navy text-white text-2xl font-bold flex items-center justify-center">1</span>
                    </div>
                    <h4 class="text-xl font-bold text-fh-navy mb-4">Diagnóstico Inicial</h4>
                    <p class="text-fh-mediumgray">Avaliação personalizada dos impactos da Reforma Tributária na sua empresa</p>
                </div>
                
                <div class="flex-1 bg-fh-navy/5 p-8 rounded-lg border-t-4 border-fh-green relative">
                    <div class="absolute -left-4 top-1/2 transform -translate-y-1/2 hidden md:block">
                        <svg class="w-8 h-8 text-fh-green arrow-animation" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div class="mb-4">
                        <span class="inline-block w-16 h-16 rounded-full bg-fh-navy text-white text-2xl font-bold flex items-center justify-center">2</span>
                    </div>
                    <h4 class="text-xl font-bold text-fh-navy mb-4">Plano de Ação</h4>
                    <p class="text-fh-mediumgray">Desenvolvimento de estratégia tributária personalizada para sua empresa</p>
                </div>
                
                <div class="flex-1 bg-fh-navy/5 p-8 rounded-lg border-t-4 border-fh-green relative">
                    <div class="absolute -left-4 top-1/2 transform -translate-y-1/2 hidden md:block">
                        <svg class="w-8 h-8 text-fh-green arrow-animation" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div class="mb-4">
                        <span class="inline-block w-16 h-16 rounded-full bg-fh-navy text-white text-2xl font-bold flex items-center justify-center">3</span>
                    </div>
                    <h4 class="text-xl font-bold text-fh-navy mb-4">Implementação</h4>
                    <p class="text-fh-mediumgray">Execução coordenada para garantir conformidade e maximizar benefícios</p>
                </div>
            </div>
            
            <div class="bg-fh-navy text-white p-8 rounded-lg max-w-4xl">
                <h4 class="text-2xl font-bold mb-4">Entre em contato agora</h4>
                <p class="text-lg mb-6">Agende uma consulta inicial gratuita e descubra como podemos transformar os desafios da Reforma Tributária em oportunidades para o seu negócio.</p>
                
                <div class="flex flex-col sm:flex-row gap-4 justify-center mt-6">
                    <button class="btn btn-lg bg-fh-green border-none hover:bg-opacity-90 text-white px-8">
                        Agendar Consultoria
                    </button>
                    <button class="btn btn-lg bg-white text-fh-navy border-none hover:bg-opacity-90 px-8">
                        Solicitar Material
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
""")

with open('slide7.html', 'w', encoding='utf-8') as f:
    f.write("""<!-- SLIDE 7: Conclusão -->
<div class="slide bg-white" id="slide7">
    <div class="h-full flex flex-col">
        <header class="bg-fh-navy p-4">
            <div class="flex items-center">
                <div class="bg-fh-navy p-2 rounded-lg">
                    <span class="text-fh-green text-2xl font-bold">FH</span>
                </div>
                <h2 class="text-white text-xl ml-4">Conclusão</h2>
            </div>
        </header>
        
        <div class="flex-grow p-10 flex flex-col items-center justify-center">
            <div class="w-full max-w-4xl">
                <div class="flex items-center justify-center mb-12">
                    <div class="flex items-center">
                        <div class="bg-fh-navy p-4 rounded-lg">
                            <span class="text-fh-green text-4xl font-bold">FH</span>
                        </div>
                        <div class="ml-4">
                            <span class="text-fh-green text-4xl font-bold">SOUZA.</span>
                            <span class="block text-fh-navy text-xl tracking-widest">ADVOGADOS</span>
                        </div>
                    </div>
                </div>
                
                <div class="bg-gradient-to-r from-fh-navy to-fh-navy/80 text-white p-8 rounded-lg mb-10">
                    <h3 class="text-2xl font-bold mb-6 text-center">A Reforma Tributária representa tanto desafio quanto oportunidade</h3>
                    <p class="text-lg text-center mb-6">
                        A escolha entre os cenários está nas suas mãos. Nossa missão é garantir que sua empresa não apenas sobreviva à transição, mas saia fortalecida e com vantagens competitivas.
                    </p>
                    <div class="flex justify-center">
                        <svg class="w-32 h-32" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="40" fill="none" stroke="#d2d5d0" stroke-width="8" />
                            <path d="M50 10 A40 40 0 0 1 90 50" stroke="#8bc53f" stroke-width="8" fill="none" />
                            <path d="M90 50 A40 40 0 0 1 70 85" stroke="#6d7681" stroke-width="8" fill="none" />
                            <path d="M70 85 A40 40 0 0 1 30 85" stroke="#1e3243" stroke-width="8" fill="none" />
                            <path d="M30 85 A40 40 0 0 1 10 50" stroke="#d2d5d0" stroke-width="8" fill="none" />
                        </svg>
                    </div>
                </div>
                
                <div class="text-center">
                    <h4 class="text-xl font-bold text-fh-navy mb-4">Contato</h4>
                    <div class="flex flex-col sm:flex-row gap-6 justify-center items-center">
                        <div class="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-fh-green mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                            </svg>
                            <span>(11) 3000-0000</span>
                        </div>
                        <div class="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-fh-green mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <span>contato@fhsouza.com.br</span>
                        </div>
                        <div class="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-fh-green mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span>São Paulo - SP</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""")

# Modificar o combine_slides.py para incluir todos os 7 slides
with open('combine_slides.py', 'w', encoding='utf-8') as f:
    f.write("""
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
""")

# Modificar o app.py para executar o combinador de slides antes de iniciar o servidor
with open('app.py', 'w', encoding='utf-8') as f:
    f.write("""
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Timer
import subprocess

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
    
    # Combinar os slides
    print("Combinando slides...")
    try:
        subprocess.run(["python", "combine_slides.py"], check=True)
    except subprocess.CalledProcessError:
        print("Erro ao combinar slides. Tentando método alternativo...")
        # Método alternativo de combinar slides caso o subprocess falhe
        from combine_slides import combine_slides
        combine_slides()
    
    print("Iniciando servidor web...")
    server = HTTPServer(('localhost', 8000), MyHandler)
    print("Abrindo navegador...")
    Timer(1, open_browser).start()
    try:
        print("Servidor rodando em http://localhost:8000")
        print("Pressione Ctrl+C para fechar o servidor")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nDesligando servidor...")
        server.shutdown()

if __name__ == "__main__":
    main()
""")

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
    
    # Combinar os slides
    print("Combinando slides...")
    try:
        subprocess.run(["python", "combine_slides.py"], check=True)
    except Exception as e:
        print(f"Erro ao combinar slides: {e}")
        print("Tentando método alternativo...")
        # Método alternativo de combinar slides caso o subprocess falhe
        try:
            from combine_slides import combine_slides
            combine_slides()
        except Exception as e:
            print(f"Erro no método alternativo: {e}")
    
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
