import express from "express";
import path from "path";
import fs from "fs";
import { createServer as createViteServer } from "vite";

async function startServer() {
  const app = express();
  const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3000;

  app.use(express.json());

  // API Route: Python Project Source Code Files
  app.get("/api/python-files", (req, res) => {
    try {
      const filesList = [
        "setup_project.py",
        "ev_driver_analysis/app.py",
        "ev_driver_analysis/requirements.txt",
        "ev_driver_analysis/README.md",
        "ev_driver_analysis/src/__init__.py",
        "ev_driver_analysis/src/generate_mock_data.py",
        "ev_driver_analysis/src/fetch_real_data.py",
        "ev_driver_analysis/src/data_loader.py",
        "ev_driver_analysis/src/feature_engineering.py",
        "ev_driver_analysis/src/econometrics.py",
        "ev_driver_analysis/src/ml_modeling.py",
        "ev_driver_analysis/src/visualization.py"
      ];

      const fileData = filesList.map((relPath) => {
        const fullPath = path.join(process.cwd(), relPath);
        let content = "";
        if (fs.existsSync(fullPath)) {
          content = fs.readFileSync(fullPath, "utf-8");
        }
        return {
          path: relPath,
          name: path.basename(relPath),
          content
        };
      });

      res.json({ success: true, count: fileData.length, files: fileData });
    } catch (err: any) {
      res.status(500).json({ success: false, error: err.message });
    }
  });

  // API Route: Project Information & Status
  app.get("/api/info", (req, res) => {
    res.json({
      name: "Global BEV Adoption Drivers Analysis Platform",
      version: "2.0.0",
      description: "Unified Econometric Panel Fixed-Effects OLS & Machine Learning Platform",
      regions: ["US", "EU", "CN"],
      oems: [
        "Tesla",
        "BYD",
        "Volkswagen Group",
        "Hyundai-Kia Group",
        "BMW Group",
        "Mercedes-Benz Group",
        "Toyota"
      ],
      timeSpan: "2020-01 to 2025-12 (72 months)",
      totalObservations: 1512,
      capabilities: [
        "Panel Fixed-Effects Regression (OLS)",
        "Vector Autoregression (VAR) 12-Month IRF",
        "XGBoost Regressor with SHAP Explainability",
        "Interactive Policy & Macroeconomic Scenario Simulator",
        "Live Python Repository Inspection"
      ]
    });
  });

  // Health check
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // Vite middleware setup
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`⚡ EV Adoption Drivers Analysis Server running on http://localhost:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("Failed to start server:", err);
});

