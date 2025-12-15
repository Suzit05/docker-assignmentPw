const express = require("express")
const dotenv = require("dotenv")
dotenv.config()
const app = express()

app.get("/", (req, res) => {
    res.json({ message: "Welcome to the node assignment" })
})

app.listen(3000, () => {
    console.log("started the server..")
})