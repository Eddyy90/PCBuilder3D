import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.152.0/examples/jsm/controls/OrbitControls.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const canvas = document.getElementById('sceneCanvas');
const renderer = new THREE.WebGLRenderer({ canvas: canvas });
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

renderer.setClearColor(0xffffff, 1);

const loader = new GLTFLoader();
loader.setDRACOLoader(dracoLoader);

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

loadGLBModel('static/models/computer_parts/box/main.glb', new THREE.Vector3(0, 0, 0), (gltf) => {});

const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 1, 1).normalize();
scene.add(directionalLight);

camera.position.z = 1;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.25;
controls.screenSpacePanning = false;
controls.maxPolarAngle = Math.PI / 2;
controls.enableZoom = true;

function animate() {
    requestAnimationFrame(animate);

    controls.update();

    renderer.render(scene, camera);
}

animate();

window.addEventListener('resize', () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

const loadPartsFromAPI = async () => {
    try {
        const response = await fetch('/api/parts');
        const parts = await response.json();

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

const addPiece = (part) => {
    const modelUrl = part.model_url;
    console.log(`Carregando modelo de ${part.name} a partir de ${modelUrl}`);

    loadGLBModel(modelUrl, new THREE.Vector3(0, 0, 0), (gltf) => {
        console.log(`Modelo de ${part.name} carregado na cena`);
    });
};

loadPartsFromAPI();