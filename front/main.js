// main.js
const { app, BrowserWindow } = require("electron");
const path = require("path");
const { autoUpdater } = require("electron-updater");
const axios = require("axios");
const { spawn } = require("child_process");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  autoUpdater.checkForUpdatesAndNotify();

  // Lancer le serveur Flask avant de vérifier l'utilisateur
  const flaskProcess = spawn(path.resolve(__dirname, "..", "back", "dist","MyBusiness", "MyBusiness.exe"));
  console.log(flaskProcess)


  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask Error: ${data}`);
  });

  // Attendre un court instant pour s'assurer que le serveur est démarré
  setTimeout(() => {
    axios
      .get("http://localhost:5000/users/check_user")
      .then((response) => {
        console.log("Utilisateur trouvé :", response.data);
        mainWindow.loadFile(path.join(__dirname, "pages", response.data));
      })
      .catch((error) => {
        console.error("Erreur lors de la vérification des utilisateurs :", error);
        mainWindow.loadFile(path.join(__dirname, "pages", "index.html"));
      });
  }, 3000);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

autoUpdater.on("update-available", () => {
  console.log("Une mise à jour est disponible !");
});

autoUpdater.on("update-downloaded", () => {
  console.log("La mise à jour a été téléchargée, elle sera installée après le redémarrage.");
});

autoUpdater.on("error", (error) => {
  console.error("Erreur de mise à jour:", error);
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

