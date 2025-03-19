const { app, BrowserWindow } = require("electron");
const path = require("path");
const { autoUpdater } = require("electron-updater");
const axios = require("axios");
const { spawn } = require("child_process");

let mainWindow;
let flaskProcess;

// Ajouter un gestionnaire pour éviter les erreurs non capturées (comme JS Error occurred in the main process)
process.on('uncaughtException', (error) => {
  console.error('Erreur non capturée:', error);
  // On ne laisse pas l'application se fermer
  // Ne rien faire ou loguer l'erreur pour éviter le message d'Electron
  // Exemple: console.log(error);
});

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

  const pythonPath = app.isPackaged
    ? path.join(__dirname)
    : path.join(__dirname, "..", "back", "dist", "app.exe");

  console.log("App packagée :", app.isPackaged);
  console.log("Chemin de l'exécutable Flask :", pythonPath);

  // Démarrer Flask en arrière-plan
  flaskProcess = spawn(pythonPath);

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });

  // Ne rien faire avec les erreurs pour ne pas les afficher dans la console
  flaskProcess.stderr.on("data", (data) => {
    // Ignore the error
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
        mainWindow.loadFile(path.join(__dirname, "pages", "register.html"));
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
