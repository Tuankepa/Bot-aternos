const express = require("express");
const app = express();

app.get("/", (req, res) => res.send("Bot Aternos đang hoạt động!"));
app.listen(3000, () => console.log("Bot đã khởi động"));

setInterval(() => {
  require("https").get("https://aternos.org/server/rquzrpFK1TLm6FCq/start");
}, 60000); // Ping mỗi 60 giây
