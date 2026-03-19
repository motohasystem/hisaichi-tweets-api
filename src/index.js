import articles from "../data/articles_classified.json";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json;charset=UTF-8", ...CORS_HEADERS },
  });
}

function summarize(article) {
  const { content_html, content_text, ...rest } = article;
  return rest;
}

function parseDate(dateStr) {
  return new Date(dateStr);
}

// GET /api/articles?page=1&limit=20&search=&year=&month=&category=
function handleArticles(url) {
  const page = Math.max(1, parseInt(url.searchParams.get("page")) || 1);
  const limit = Math.min(100, Math.max(1, parseInt(url.searchParams.get("limit")) || 20));
  const search = url.searchParams.get("search") || "";
  const year = url.searchParams.get("year") || "";
  const month = url.searchParams.get("month") || "";
  const category = url.searchParams.get("category") || "";

  let filtered = articles;

  if (category) {
    filtered = filtered.filter((a) => a.category === category);
  }
  if (year) {
    filtered = filtered.filter((a) => {
      const d = parseDate(a.date);
      return d.getFullYear() === parseInt(year);
    });
  }
  if (month) {
    filtered = filtered.filter((a) => {
      const d = parseDate(a.date);
      return d.getMonth() + 1 === parseInt(month);
    });
  }
  if (search) {
    const q = search.toLowerCase();
    filtered = filtered.filter(
      (a) =>
        (a.title && a.title.toLowerCase().includes(q)) ||
        (a.description && a.description.toLowerCase().includes(q)) ||
        (a.content_text && a.content_text.toLowerCase().includes(q))
    );
  }

  const total = filtered.length;
  const totalPages = Math.ceil(total / limit);
  const start = (page - 1) * limit;
  const items = filtered.slice(start, start + limit).map((a, i) => ({
    id: articles.indexOf(a),
    ...summarize(a),
  }));

  return json({
    data: items,
    pagination: { page, limit, total, totalPages },
  });
}

// GET /api/articles/random?category=
function handleRandom(url) {
  const category = url.searchParams.get("category") || "";
  let pool = articles;

  if (category) {
    pool = pool.filter((a) => a.category === category);
  }

  if (pool.length === 0) {
    return json({ error: "No articles found" }, 404);
  }

  const idx = Math.floor(Math.random() * pool.length);
  const article = pool[idx];
  return json({
    id: articles.indexOf(article),
    ...article,
  });
}

// GET /api/articles/:id
function handleArticleById(id) {
  if (id < 0 || id >= articles.length) {
    return json({ error: "Article not found" }, 404);
  }
  return json({ id, ...articles[id] });
}

// GET /api/categories
function handleCategories() {
  const counts = {};
  for (const a of articles) {
    counts[a.category] = (counts[a.category] || 0) + 1;
  }
  const data = Object.entries(counts).map(([name, count]) => ({ name, count }));
  return json({ data });
}

// GET /api/stats
function handleStats() {
  const counts = {};
  const years = new Set();
  for (const a of articles) {
    counts[a.category] = (counts[a.category] || 0) + 1;
    const d = parseDate(a.date);
    years.add(d.getFullYear());
  }
  return json({
    totalArticles: articles.length,
    categories: counts,
    years: [...years].sort(),
  });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    if (request.method !== "GET") {
      return json({ error: "Method not allowed" }, 405);
    }

    const path = url.pathname;

    if (path === "/api/articles/random") {
      return handleRandom(url);
    }
    if (path === "/api/articles") {
      return handleArticles(url);
    }
    if (path.startsWith("/api/articles/")) {
      const id = parseInt(path.split("/").pop());
      if (isNaN(id)) {
        return json({ error: "Invalid ID" }, 400);
      }
      return handleArticleById(id);
    }
    if (path === "/api/categories") {
      return handleCategories();
    }
    if (path === "/api/stats") {
      return handleStats();
    }

    // Static assets
    return env.ASSETS.fetch(request);
  },
};
