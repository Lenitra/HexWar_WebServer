// Initialisation de la scène, de la caméra et du rendu
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  1,
  1000
);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('three-container').appendChild(renderer.domElement);

// Ajout d'une grille hexagonale
const geometry = new THREE.CircleGeometry(5, 6);
const material = new THREE.MeshBasicMaterial({ color: 0xff007f, wireframe: true });
const hexGrid = new THREE.Mesh(geometry, material);
scene.add(hexGrid);

// Position de la caméra
camera.position.z = 10;

// Animation
function animate() {
  requestAnimationFrame(animate);
  hexGrid.rotation.z += 0.005;
  renderer.render(scene, camera);
}
animate();

// Réactivité à la taille de la fenêtre
window.addEventListener('resize', () => {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
});

gsap.registerPlugin(ScrollTrigger);

// Animation du titre à l'entrée
gsap.from('.logo', { opacity: 0, y: -50, duration: 1 });

// Animations des sections
gsap.utils.toArray('section').forEach((section, i) => {
  gsap.fromTo(section, { opacity: 0 }, {
    opacity: 1,
    duration: 1,
    scrollTrigger: {
      trigger: section,
      start: 'top 80%',
      end: 'top 30%',
      toggleActions: 'play none none reverse'
    }
  });
});
