const API = location.origin.replace(':8080', ':8000');
const map = L.map('map').setView([21.028, 105.854], 12);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
const layers = { aqi: L.layerGroup().addTo(map), poi: L.layerGroup().addTo(map), weather: L.layerGroup().addTo(map) };
function aqiColor(aqi){ if (aqi==null) return '#999'; if (aqi<=50) return '#2ecc71'; if (aqi<=100) return '#f1c40f'; if (aqi<=150) return '#e67e22'; if (aqi<=200) return '#e74c3c'; return '#8e44ad'; }
async function loadAQI(){ layers.aqi.clearLayers(); const res=await fetch(`${API}/api/aqi`); const data=await res.json();
  data.forEach(d=>{ const m=L.circleMarker([d.coords[1], d.coords[0]], { radius:7, weight:2, color: aqiColor(d.aqi) });
    m.bindPopup(`<b>AQI:</b> ${d.aqi ?? 'N/A'}<br/><b>PM2.5:</b> ${d.pm25 ?? 'N/A'}<br/><b>Thời gian:</b> ${d.dateObserved ?? ''}`); layers.aqi.addLayer(m); });}
async function loadPOI(){ layers.poi.clearLayers(); const res=await fetch(`${API}/api/poi`); const data=await res.json();
  data.forEach(d=>{ const m=L.marker([d.coords[1], d.coords[0]]); m.bindPopup(`<b>${d.name ?? 'POI'}</b><br/><i>${d.category}</i>`); layers.poi.addLayer(m); });}
async function loadWeather(){ layers.weather.clearLayers(); const res=await fetch(`${API}/api/weather`); const data=await res.json();
  data.forEach(d=>{ const m=L.circleMarker([d.coords[1], d.coords[0]], { radius:6, weight:1 }); m.bindPopup(`<b>Nhiệt độ:</b> ${d.temperature ?? 'N/A'} °C<br/><b>Độ ẩm:</b> ${d.humidity ?? 'N/A'}%`); layers.weather.addLayer(m); });}
function wireToggles(){ const aqi=document.getElementById('layer-aqi'); const poi=document.getElementById('layer-poi'); const weather=document.getElementById('layer-weather');
  aqi.addEventListener('change', ()=> aqi.checked? layers.aqi.addTo(map): map.removeLayer(layers.aqi));
  poi.addEventListener('change', ()=> poi.checked? layers.poi.addTo(map): map.removeLayer(layers.poi));
  weather.addEventListener('change', ()=> weather.checked? layers.weather.addTo(map): map.removeLayer(layers.weather));}
async function refresh(){ await Promise.all([loadAQI(), loadPOI(), loadWeather()]); }
wireToggles(); refresh(); setInterval(refresh, 120000);
