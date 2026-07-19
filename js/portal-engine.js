/* 
 * portal-engine.js
 * DYNAMIC TIME ENGINE & TSA/RSA CRYPTOGRAPHIC SIGNATURE EMULATOR
 * Built for wongkelvin.com (design-03 Master Edition)
 */

document.addEventListener('DOMContentLoaded', () => {
  const secRing = document.getElementById('sec-ring');
  const minRing = document.getElementById('min-ring');
  const hrsRing = document.getElementById('hrs-ring');
  const localTimeDisplay = document.getElementById('local-digital-time');
  const tyoTimeDisplay = document.getElementById('tokyo-time');
  const lonTimeDisplay = document.getElementById('london-time');
  const nycTimeDisplay = document.getElementById('new-york-time');
  const tsaHashNode = document.getElementById('tsa-hash-node');

  // 1. Hands-Free SVG Concentric Clock Engine
  function runConcentricClock() {
    const now = new Date();
    
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const milliseconds = now.getMilliseconds();

    // Fluid fractional time representation
    const secFloat = seconds + (milliseconds / 1000);
    const minFloat = minutes + (secFloat / 60);
    const hrsFloat = (hours % 12) + (minFloat / 60);

    // Map time coordinates to circular SVG stroke-dashoffset parameters
    // Seconds: Radius = 45 -> Circumference = 283
    const secOffset = 283 - (secFloat / 60) * 283;
    // Minutes: Radius = 41 -> Circumference = 257
    const minOffset = 257 - (minFloat / 60) * 257;
    // Hours: Radius = 37 -> Circumference = 232
    const hrsOffset = 232 - (hrsFloat / 12) * 232;

    if (secRing) secRing.style.strokeDashoffset = secOffset;
    if (minRing) minRing.style.strokeDashoffset = minOffset;
    if (hrsRing) hrsRing.style.strokeDashoffset = hrsOffset;

    // Update Digital Local Time
    const pad = (n) => String(Math.floor(n)).padStart(2, '0');
    if (localTimeDisplay) {
      localTimeDisplay.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
    }

    // 2. World Timezone Dynamic Calculators (Dynamic UTC offset mapping)
    const getTzTime = (offset) => {
      const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
      const targetTime = new Date(utcTime + (3600000 * offset));
      return `${pad(targetTime.getHours())}:${pad(targetTime.getMinutes())}`;
    };

    if (tyoTimeDisplay) tyoTimeDisplay.textContent = getTzTime(9);   // Tokyo (UTC+9)
    if (lonTimeDisplay) lonTimeDisplay.textContent = getTzTime(1);   // London (UTC+1/BST)
    if (nycTimeDisplay) nycTimeDisplay.textContent = getTzTime(-4);  // New York (UTC-4/EDT)
  }

  // 3. TSA/RSA Real-Time Cryptographical Handshake Simulator
  function updateCryptographicSignatures() {
    const hexPool = "0123456789ABCDEF";
    const blockId = Math.floor(Date.now() / 10000); // Dynamic Block ID tick every 10 seconds
    
    // Generate a secure mock 64-character hash sequence
    let mockHash = "";
    for (let i = 0; i < 32; i++) {
      mockHash += hexPool.charAt(Math.floor(Math.random() * hexPool.length));
    }
    
    // Generate a mini verification signature index
    let verifiedSig = "";
    for (let i = 0; i < 6; i++) {
      verifiedSig += hexPool.charAt(Math.floor(Math.random() * hexPool.length));
    }

    if (tsaHashNode) {
      tsaHashNode.innerHTML = `
        <span class="text-brand-red font-bold font-mono">BLOCK #${blockId}</span> | 
        <span class="text-neon-cyan">HASH::${mockHash.substring(0, 10)}...${mockHash.substring(22)}</span> | 
        <span class="text-neon-green font-mono">[0x${verifiedSig}] VERIFIED</span>
      `;
    }
  }

  // Execution frequency setups
  setInterval(runConcentricClock, 50); // Fluid high-frequency updates for sub-second sweeps
  setInterval(updateCryptographicSignatures, 300); // 300ms verification polling cycles
  
  runConcentricClock();
  updateCryptographicSignatures();
});

// 4. Modal Overlays
function toggleQR() {
  const qrModal = document.getElementById('qr-modal');
  if (qrModal) qrModal.classList.toggle('hidden');
}

// Escape key listener to close overlay modals
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    const qrModal = document.getElementById('qr-modal');
    if (qrModal && !qrModal.classList.contains('hidden')) {
      qrModal.classList.add('hidden');
    }
  }
});

// Expose toggle functions globally for button triggers
window.toggleQR = toggleQR;
