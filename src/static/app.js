const map = L.map("map", { worldCopyJump: true, minZoom: 2 }).setView([12, -20], 2);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 8,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

const audioButton = document.getElementById("audio-button");
const audioStatus = document.getElementById("audio-status");
const dataStatus = document.getElementById("data-status");
const detail = document.getElementById("earthquake-detail");
const rankingList = document.getElementById("ranking");
const sourceLink = document.getElementById("source-link");

const scale = ["C", "D", "Eb", "G", "A"];
const panner = new Tone.Panner(0).toDestination();
const reverb = new Tone.Reverb({ decay: 3.5, wet: 0.35 }).connect(panner);
const synth = new Tone.FMSynth({
  harmonicity: 1.5,
  modulationIndex: 8,
  envelope: { attack: 0.04, decay: 0.35, sustain: 0.25, release: 2.2 },
  modulationEnvelope: { attack: 0.02, decay: 0.3, sustain: 0.2, release: 1.4 },
}).connect(reverb);

let audioReady = false;

async function enableAudio() {
  if (!audioReady) {
    await Tone.start();
    await reverb.generate();
    audioReady = true;
  }
  audioButton.textContent = "Audio activado";
  audioButton.classList.add("is-active");
  audioStatus.textContent = "Pulsa cualquier terremoto para escucharlo";
}

audioButton.addEventListener("click", enableAudio);

function clamp(value, minimum, maximum) {
  return Math.min(Math.max(value, minimum), maximum);
}

function sonificationFor(feature) {
  const { mag } = feature.properties;
  const [longitude, latitude, depth = 0] = feature.geometry.coordinates;
  const noteIndex = clamp(Math.floor(((latitude + 90) / 180) * scale.length), 0, scale.length - 1);
  const octave = clamp(5 - Math.floor(depth / 100), 2, 5);

  return {
    note: `${scale[noteIndex]}${octave}`,
    duration: 0.7 + (mag - 8.5) * 1.5,
    volume: clamp(-13 + (mag - 8.5) * 10, -13, -2),
    pan: clamp(longitude / 180, -1, 1),
  };
}

async function playEarthquake(feature) {
  await enableAudio();
  const sound = sonificationFor(feature);
  panner.pan.rampTo(sound.pan, 0.12);
  synth.volume.rampTo(sound.volume, 0.08);
  synth.triggerAttackRelease(sound.note, sound.duration);
  return sound;
}

function formatDate(timestamp) {
  return new Intl.DateTimeFormat("es", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(timestamp));
}

function rankFeatures(features) {
  let previousMagnitude = null;
  let currentRank = 0;
  return features.map((feature, index) => {
    const magnitude = feature.properties.mag;
    if (magnitude !== previousMagnitude) currentRank = index + 1;
    previousMagnitude = magnitude;
    return { feature, rank: currentRank };
  });
}

function markerIcon(magnitude) {
  const size = 18 + (magnitude - 8.5) * 25;
  const hue = 28 - (magnitude - 8.5) * 18;
  return L.divIcon({
    className: "quake-marker-shell",
    html: `<span class="quake-marker" style="--size:${size}px;--hue:${hue}">${magnitude.toFixed(1)}</span>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}

function showDetail(feature, rank, sound) {
  const { mag, magType, place, time, url } = feature.properties;
  const [longitude, latitude, depth = 0] = feature.geometry.coordinates;
  const panLabel = sound.pan < -0.15 ? "izquierda" : sound.pan > 0.15 ? "derecha" : "centro";

  detail.innerHTML = `
    <p class="section-kicker">Puesto ${rank}</p>
    <div class="magnitude-badge">${(magType || "M").toUpperCase()} ${mag.toFixed(1)}</div>
    <h2>${place}</h2>
    <p class="event-date">${formatDate(time)}</p>
    <dl class="event-data">
      <div><dt>Profundidad</dt><dd>${depth.toFixed(1)} km</dd></div>
      <div><dt>Coordenadas</dt><dd>${latitude.toFixed(2)}, ${longitude.toFixed(2)}</dd></div>
      <div><dt>Nota</dt><dd>${sound.note}</dd></div>
      <div><dt>Estéreo</dt><dd>${panLabel}</dd></div>
    </dl>
    <a class="usgs-link" href="${url}" target="_blank" rel="noreferrer">Ver ficha oficial en USGS ↗</a>
  `;
}

function addEarthquake(feature, rank, bounds) {
  const { mag, place } = feature.properties;
  const [longitude, latitude] = feature.geometry.coordinates;
  const marker = L.marker([latitude, longitude], {
    icon: markerIcon(mag),
    title: `${place}, Mw ${mag}`,
  }).addTo(map);

  marker.bindTooltip(`#${rank} · Mw ${mag.toFixed(1)} · ${place}`);
  marker.on("click", async () => {
    const sound = await playEarthquake(feature);
    showDetail(feature, rank, sound);
  });

  bounds.push([latitude, longitude]);
}

function addRankingItem(feature, rank) {
  const { mag, place, time } = feature.properties;
  const item = document.createElement("li");
  item.innerHTML = `
    <button type="button" class="ranking-item">
      <span class="rank">${rank}</span>
      <span class="ranking-copy"><strong>${place}</strong><small>${formatDate(time)}</small></span>
      <span class="ranking-mag">Mw ${mag.toFixed(1)}</span>
    </button>
  `;
  item.querySelector("button").addEventListener("click", async () => {
    const [longitude, latitude] = feature.geometry.coordinates;
    map.flyTo([latitude, longitude], 4, { duration: 1.2 });
    const sound = await playEarthquake(feature);
    showDetail(feature, rank, sound);
  });
  rankingList.appendChild(item);
}

async function loadEarthquakes() {
  try {
    const response = await fetch("/earthquakes?limit=20");
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "No fue posible consultar USGS");

    const ranked = rankFeatures(data.features);
    const bounds = [];
    ranked.forEach(({ feature, rank }) => {
      addEarthquake(feature, rank, bounds);
      addRankingItem(feature, rank);
    });

    if (bounds.length) map.fitBounds(bounds, { padding: [30, 30], maxZoom: 3 });
    rankingList.setAttribute("aria-busy", "false");
    dataStatus.textContent = `${data.features.length} eventos · desde 1900`;
    if (data.metadata.query_url) sourceLink.href = data.metadata.query_url;
  } catch (error) {
    dataStatus.textContent = "USGS no disponible";
    dataStatus.classList.add("is-error");
    rankingList.setAttribute("aria-busy", "false");
    rankingList.innerHTML = `<li class="load-error"><strong>No pudimos cargar el catálogo.</strong><span>${error.message}</span></li>`;
  }
}

loadEarthquakes();
