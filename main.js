const { app, BrowserWindow, autoUpdater, ipcMain, dialog } = require("electron");
const path = require("path");
const url = require("url")
require('dotenv').config();
const { platform, env } = process
let mainWindow = null;

const createMainWindow = () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    darkTheme: true,
    webPreferences: {
      nodeIntegration: true
  }
  });

  if (env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools()
  }

  mainWindow.loadURL(`file://${__dirname}/templates/login.html`);

  ipcMain.on("error", (event) => {
    mainWindow.loadURL(`file://${__dirname}/templates/login.html`)
  })

  ipcMain.on("user", async (event) => {
    mainWindow.loadURL(`file://${__dirname}/templates/user.html`)

    if (env.NODE_ENV === 'development') {
      return // Skip updates on development env
    }

  });


  ipcMain.on("admin", async (event) => {
    mainWindow.loadURL(`file://${__dirname}/templates/admin.html`)

    if (env.NODE_ENV === 'development') {
      return // Skip updates on development env
    }

  });

  mainWindow.on("closed", function() {
    mainWindow = null;
  });
};

app.on("ready", createMainWindow);
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
      app.quit();
  }
});
app.on("browser-window-created", function(e, window) {
  window.setMenu(null);
});
app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
app.on("quit", function() {
});