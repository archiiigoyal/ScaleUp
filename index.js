import express from "express";
import cors from "cors";
import "dotenv/config";
import { ApifyClient } from "apify-client";
import axios from "axios";

const app = express();
app.use(cors());
app.use(express.json());
const USERNAME = "cromila_";

const client = new ApifyClient({
  token: process.env.APIFY_TOKEN
});


import loginRoutes from "./routes/login.routes.js";
app.use(express.static("frontend")); // serve HTML files

app.use("/api", loginRoutes);

app.post("/scrape", async (req, res) => {
  const { username } = req.body;

  try {
    const run = await client.actor("apify/instagram-scraper").call({
      directUrls: [`https://www.instagram.com/${USERNAME}/`],
      resultsLimit: 20,
      scrapePosts: true,
      scrapeComments: true
    });

    const { items } = await client.dataset(run.defaultDatasetId).listItems();

    const comments = items
      .flatMap(post => post.latestComments || [])
      .map(c => typeof c.text === "string" ? c.text.trim() : null)
      .filter(Boolean);

    const analysisResponse = await axios.post(
      "http://127.0.0.1:8000/analyze-competitor",
      { comments }
    );

    res.json(analysisResponse.data);

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => {
  console.log("Server running at http://localhost:5000");
});
