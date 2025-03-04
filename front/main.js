// main.js
const { app, BrowserWindow } = require("electron");
const path = require("path");
const axios = require("axios");

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

  // Exemple de vérification d'utilisateur via votre API Flask (déjà lancée manuellement)
  axios
    .get("http://localhost:5000/users/check_user")
    .then((response) => {
      console.log("Utilisateur trouvé :", response.data);
      // Chargez la page correspondante en fonction de la réponse,
      // par exemple response.data peut être le nom du fichier HTML à charger
      mainWindow.loadFile(path.join(__dirname, "pages", response.data));
    })
    .catch((error) => {
      console.error("Erreur lors de la vérification des utilisateurs :", error);
      // Si l'API n'est pas disponible, chargez une page par défaut
      mainWindow.loadFile(path.join(__dirname, "pages", "index.html"));
    });

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

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
