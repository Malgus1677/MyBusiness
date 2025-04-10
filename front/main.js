const { app, BrowserWindow, Menu } = require("electron");
const path = require("path");
const { autoUpdater } = require("electron-updater");
const axios = require("axios");


let mainWindow;


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
  });

  mainWindow.setMenu(null); // Supprimer la barre de menu par défaut
  

  autoUpdater.checkForUpdatesAndNotify();


  // Attendre un court instant pour s'assurer que le serveur est démarré
  setTimeout(() => {
    axios
      .get("http://69.62.111.132/mybusiness/users/check_user")
      .then((response) => {
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
