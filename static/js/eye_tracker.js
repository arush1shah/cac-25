window.addEventListener("load", async () => {
    console.log("🧠 WebGazer loading...");
    localStorage.removeItem("webgazer_calibrated");
    webgazer.clearData();
    
    await webgazer
      .setRegression("ridge")
      .setTracker("clmtrackr")
      .showVideo(true)
      .showFaceOverlay(true)
      .showFaceFeedbackBox(true)
      .showPredictionPoints(false)
      .begin();
  
    // --- Re-apply styles repeatedly so overlays never block clicks ---
    const lockOverlayStyle = () => {
      ["webgazerVideoFeed", "webgazerFaceOverlay", "webgazerFaceFeedbackBox"].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          Object.assign(el.style, {
            position: "fixed",
            top: "10px",
            right: "10px",
            width: "220px",
            height: "165px",
            zIndex: 9999,
            pointerEvents: "none",
            transform: "none",
          });
          el.style.setProperty("pointer-events", "none", "important");
          el.style.setProperty("z-index", "9999", "important");
        }
      });
    };
    // Call several times since WebGazer rebuilds elements dynamically
    [500, 1500, 3000, 5000].forEach(t => setTimeout(lockOverlayStyle, t));
  
    // --- Calibration setup ---
    const runCalibration = async () => {
      const points = [
        [60, 60], [window.innerWidth / 2, 60], [window.innerWidth - 60, 60],
        [60, window.innerHeight / 2], [window.innerWidth / 2, window.innerHeight / 2], [window.innerWidth - 60, window.innerHeight / 2],
        [60, window.innerHeight - 60], [window.innerWidth / 2, window.innerHeight - 60], [window.innerWidth - 60, window.innerHeight - 60]
      ];
  
      for (const [x, y] of points) {
        const dot = document.createElement("div");
        Object.assign(dot.style, {
          position: "fixed",
          left: `${x - 12}px`,
          top: `${y - 12}px`,
          width: "24px",
          height: "24px",
          background: "#e85d04",
          borderRadius: "50%",
          zIndex: 20000,
          cursor: "pointer"
        });
        document.body.appendChild(dot);
  
        await new Promise(res => {
          dot.addEventListener("click", () => {
            const interval = setInterval(() => {
              webgazer.recordScreenPosition(x, y);
            }, 100);
            setTimeout(() => {
              clearInterval(interval);
              dot.remove();
              res();
            }, 1000);
          }, { once: true });
        });
      }
      alert("✅ Calibration complete");
      localStorage.setItem("webgazer_calibrated", "true");
    };
  
    // --- Start calibration if not yet done ---
    if (!localStorage.getItem("webgazer_calibrated")) {
      alert("Click the orange dots to calibrate your eye tracking.");
      await runCalibration();
    }
  
    // --- Attention tracking ---
    const summary = document.getElementById("summary-output");
    const gazeDot = document.createElement("div");
    Object.assign(gazeDot.style, {
      position: "fixed",
      width: "12px",
      height: "12px",
      backgroundColor: "#e85d04",
      borderRadius: "50%",
      pointerEvents: "none",
      zIndex: 15000
    });
    document.body.appendChild(gazeDot);
  
    let smoothX = window.innerWidth / 2, smoothY = window.innerHeight / 2;
    let lastSeen = Date.now(), glowing = false;
  
    const glowOn = () => {
      summary.style.boxShadow = "0 0 40px 12px rgba(232,93,4,0.7)";
    };
    const glowOff = () => { summary.style.boxShadow = "none"; };
  
    webgazer.setGazeListener((data) => {
      if (data) {
        smoothX = 0.85 * smoothX + 0.15 * data.x;
        smoothY = 0.85 * smoothY + 0.15 * data.y;
        gazeDot.style.left = `${smoothX}px`;
        gazeDot.style.top = `${smoothY}px`;
        lastSeen = Date.now();
        if (glowing) { glowOff(); glowing = false; }
      }
    });
  
    setInterval(() => {
      const tracker = webgazer.getTracker();
      const pos = tracker ? tracker.getCurrentPosition() : null;
      if ((!pos || pos === false) && Date.now() - lastSeen > 10000 && !glowing) {
        glowing = true;
        glowOn();
        console.log("⚠️ You looked away for 10s");
      }
    }, 1000);
  });
  