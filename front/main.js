const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const axios = require("axios");

let flaskProcess;
let mainWindow;

const workDir = path.join(__dirname, '..', 'back');
console.log("Répertoire de travail pour Flask:", workDir);

function startFlask() {
    console.log("Démarrage du serveur Flask...");
const flaskProcess = spawn('python', ['app.py'], {
    cwd: workDir,  // Spécifie le répertoire de travail
    shell: true,
    stdio: 'inherit',
});


    flaskProcess.on("error", (err) => {
        console.error("Erreur lors du démarrage de Flask :", err);
    });

    flaskProcess.on("exit", (code) => {
        console.log(`Flask s'est arrêté avec le code ${code}`);
    });

    flaskProcess.on('close', (code) => {
        if (code === 0) {
            console.log('Le serveur Flask s\'est arrêté proprement.');
        } else {
            console.error(`Le serveur Flask a échoué avec le code de sortie ${code}`);
        }
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            nodeIntegration: true
        }
    });

    checkIfUserExists();

    mainWindow.on("closed", () => {
        mainWindow = null;
    });
}

function checkIfUserExists() {
    axios.get('http://localhost:5000/users/check_user')
        .then((response) => {
            console.log("Utilisateur trouvé :", response.data);
           mainWindow.loadFile(path.join(__dirname, 'pages',response.data));
            
        })
        .catch((error) => {
            console.error("Erreur lors de la vérification des utilisateurs :", error);
        });
}

app.whenReady().then(() => {
    startFlask();
    setTimeout(createWindow, 3000); // Attente pour s'assurer que Flask démarre
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        if (flaskProcess) flaskProcess.kill();
        app.quit();
    }
});

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
