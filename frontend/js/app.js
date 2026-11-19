const API = "http://127.0.0.1:8000/api/analyse";
const $ = (id) => document.getElementById(id);

$("photo").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  $("preview").src = URL.createObjectURL(file);
  $("analysis").hidden = false;
  $("attrs").innerHTML = "";
  $("status").textContent = `Selected: ${file.name}`;
});

function el(tag, props = {}, children = []) {
  const node = Object.assign(document.createElement(tag), props);
  children.forEach((c) => node.append(c));
  return node;
}

function shortLabel(label) {
  return label.replace(/^(a|an) /, "").replace(/ hoodie$/, "").replace(/^hoodie with /, "");
}

function showAttributes(a) {
  const list = $("attrs");
  list.innerHTML = "";
  const row = (name, text, conf) => {
    const li = el("li", {}, [el("b", { textContent: name }), text]);
    if (conf !== null && conf !== undefined && conf < 0.6) {
      li.append(" ", el("span", { className: "unsure", textContent: `(${Math.round(conf * 100)}% sure)` }));
    }
    list.append(li);
  };

  const swatch = el("span", { className: "swatch" });
  swatch.style.background = a.colour.hex;
  const colourLi = el("li", {}, [el("b", { textContent: "Colour" }), swatch, a.colour.name]);
  list.append(colourLi);

  row("Style", shortLabel(a.closure.label), a.closure.confidence);
  row("Fit", shortLabel(a.fit.label), a.fit.confidence);
  row("Pattern", shortLabel(a.pattern.label), a.pattern.confidence);
  row("Logo", shortLabel(a.logo.label), a.logo.confidence);
  row("Size", $("size").value || "choose your size above", null);
}

function showResults(results) {
  const grid = $("results");
  grid.innerHTML = "";
  if (!results.length) {
    $("status").textContent = "No matches yet - try a higher max price or index more hoodies.";
    return;
  }
  results.forEach((p) => {
    const img = el("img", { src: p.image || "", alt: p.name || "Hoodie", loading: "lazy" });
    img.onerror = () => { img.style.visibility = "hidden"; };
    const price = Number(p.price);
    const card = el("article", { className: "card" }, [
      img,
      el("div", { className: "body" }, [
        el("h3", { textContent: p.name || "Hoodie" }),
        el("span", { className: "store", textContent: p.store || p.brand || "" }),
        el("span", { className: "price",
          textContent: isNaN(price) ? "" : `${p.currency === "GBP" || !p.currency ? "£" : p.currency + " "}${price.toFixed(2)}` }),
        el("span", { className: "match",
          textContent: `${Math.round((p.similarity || 0) * 100)}% match · price as of ${p.checked_on || "last scrape"}` }),
      ]),
      el("a", { href: p.url, target: "_blank", rel: "noopener", textContent: "View at retailer" }),
    ]);
    grid.append(card);
  });
  $("status").textContent = `${results.length} similar hoodies found`;
}

$("go").addEventListener("click", async () => {
  const file = $("photo").files[0];
  if (!file) { $("status").textContent = "Please choose a photo first."; return; }

  const form = new FormData();
  form.append("file", file);
  const max = $("maxPrice").value;
  const url = API + (max ? `?max_price=${encodeURIComponent(max)}` : "");

  $("go").disabled = true;
  $("status").textContent = "Analysing your photo... (this can take a few seconds)";
  $("results").innerHTML = "";

  try {
    const res = await fetch(url, { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Something went wrong");
    showAttributes(data.attributes);
    showResults(data.results);
  } catch (err) {
    $("status").textContent = err.message.includes("Failed to fetch")
      ? "Can't reach the server - is uvicorn running?"
      : `Error: ${err.message}`;
  } finally {
    $("go").disabled = false;
  }
});