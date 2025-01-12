import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.152.0/examples/jsm/controls/OrbitControls.js';

// Instanciar o DRACOLoader e configurar o caminho para o decoder
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');

// Criar a cena, câmera e renderizador
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Selecionar o canvas no DOM (dentro do card, com id="sceneCanvas")
const canvas = document.getElementById('sceneCanvas');
const renderer = new THREE.WebGLRenderer({ canvas: canvas });
// Ajustar o tamanho do renderizador para a div onde o canvas está
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

// Definir o fundo da cena como branco
renderer.setClearColor(0xffffff, 1);

// Instanciar o carregador GLTF e associar o DRACOLoader
const loader = new GLTFLoader();
loader.setDRACOLoader(dracoLoader);

// Função para carregar o modelo GLB
const loadGLBModel = (url, position = new THREE.Vector3(0, 0, 0), callback) => {
    loader.load(
        url,
        (gltf) => {
            gltf.scene.position.set(position.x, position.y, position.z);
            scene.add(gltf.scene);
            callback(gltf.scene);
        },
        undefined,
        (error) => {
            console.error('Erro ao carregar o modelo GLB:', error);
        }
    );
};

// Carregar o modelo do gabinete
loadGLBModel('static/models/computer_parts/box/main.glb', new THREE.Vector3(0, 0, 0), (gltf) => {});

// Adicionar iluminação
const ambientLight = new THREE.AmbientLight(0x404040); // Luz ambiente
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // Luz direcional
directionalLight.position.set(1, 1, 1).normalize();
scene.add(directionalLight);

// Posicionar a câmera
camera.position.z = 1;

// Criar os controles de órbita (controle do mouse)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Ativar o amortecimento para um movimento mais suave
controls.dampingFactor = 0.25; // Fator de amortecimento (ajuste conforme necessário)
controls.screenSpacePanning = false; // Impedir o movimento de pan (movimento da cena para a esquerda/direita)
controls.maxPolarAngle = Math.PI / 2; // Limitar o movimento vertical da câmera (evita virar o modelo para baixo)
controls.enableZoom = true; // Permitir o zoom com o scroll do mouse

// Função de animação para atualizar e renderizar a cena
function animate() {
    requestAnimationFrame(animate);

    // Atualizar os controles de órbita
    controls.update(); // Necessário para que o amortecimento funcione

    // Renderizar a cena
    renderer.render(scene, camera);
}

animate();

// Redimensionar o canvas quando a janela for redimensionada
window.addEventListener('resize', () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

// Função para carregar as peças da API
const loadPartsFromAPI = async () => {
    try {
        const response = await fetch('/api/parts');
        const parts = await response.json();

        // Para cada peça, adicionar um botão
        const partsContainer = document.querySelector('.menu-container');
        parts.forEach(part => {
            const button = document.createElement('button');
            button.classList.add('btn', 'btn-primary', 'w-100', 'mb-2');
            button.textContent = `Adicionar ${part.name}`;
            button.onclick = () => addPiece(part);
            partsContainer.appendChild(button);
        });
    } catch (error) {
        console.error('Erro ao carregar as peças:', error);
    }
};

// Função para adicionar uma peça à cena
const addPiece = (part) => {
    const modelUrl = `static/models/computer_parts/${part.category.toLowerCase()}/${part.model}`;
    loadGLBModel(modelUrl, new THREE.Vector3(0, 0, 0), (gltf) => {
        console.log(`Modelo de ${part.name} carregado`);
    });
};

// Chamar a função para carregar as peças da API assim que a página for carregada
loadPartsFromAPI();