<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Weather App</title>
  <style>
    :root{--bg:#071331;--card:#0f2a4a;--accent:#2fb3ff;--glass:rgba(255,255,255,0.04);--muted:#9fb6d6}
    *{box-sizing:border-box;font-family:Inter,system-ui,Segoe UI,Roboto,"Helvetica Neue",Arial}
    body{margin:0;min-height:100vh;background:linear-gradient(135deg,#06223f 0%,#021028 100%);color:#e6f4ff;display:flex;align-items:center;justify-content:center;padding:24px}
    .app{width:100%;max-width:900px;background:linear-gradient(180deg,rgba(255,255,255,0.03),transparent);border-radius:18px;padding:22px;display:grid;grid-template-columns:1fr 360px;gap:20px;box-shadow:0 10px 30px rgba(2,8,23,0.7)}
    header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between}
    h1{margin:0;font-size:20px;letter-spacing:0.2px}
    .left{padding:18px}
    .controls{display:flex;gap:10px;align-items:center}
    input[type=text]{padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);background:var(--glass);color:inherit;min-width:220px}
    button{background:var(--accent);border:none;padding:10px 12px;border-radius:10px;cursor:pointer;color:#012034;font-weight:600}
    .small{font-size:13px;color:var(--muted)}
    .card{background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent);padding:18px;border-radius:12px;border:1px solid rgba(255,255,255,0.03)}
    .weather-main{display:flex;gap:18px;align-items:center}
    .weather-main img{width:110px;height:110px}
    .temp{font-size:44px;font-weight:700;margin:0}
    .desc{margin:4px 0;font-weight:600}
    .meta{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}
    .meta .item{background:rgba(255,255,255,0.02);padding:8px 10px;border-radius:8px;font-size:13px}
    .right{padding:18px}
    .right .stats{display:flex;flex-direction:column;gap:10px}
    .stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-radius:8px;background:rgba(255,255,255,0.02)}
    .footer{grid-column:1/-1;text-align:right;font-size:13px;color:var(--muted);margin-top:6px}
    @media (max-width:880px){.app{grid-template-columns:1fr;max-width:520px}.right{order:2}.left{order:1}}
  </style>
</head>
<body>
  <div class="app" role="application" aria-label="Weather app">
    <header>
      <h1>Weather App</h1>
      <div class="small">Shows current weather by location or by search</div>
    </header>

    <section class="left">
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
          <div class="controls">
            <input id="cityInput" type="text" placeholder="Enter city or city,country (e.g. Karachi or London,GB)" aria-label="city" />
            <button id="searchBtn">Search</button>
            <button id="locBtn">Use my location</button>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <label class="small">Units</label>
            <select id="unitSelect" aria-label="units">
              <option value="metric">°C</option>
              <option value="imperial">°F</option>
            </select>
          </div>
        </div>
      </div>

      <div id="result" class="card" style="margin-top:14px;min-height:150px">
        <div id="loading" class="small">Search for a city or click "Use my location"</div>
        <div id="weatherPanel" style="display:none">
          <div class="weather-main">
            <div>
              <img id="icon" alt="weather icon" src="" />
            </div>
            <div>
              <p id="temp" class="temp">--°</p>
              <p id="condition" class="desc">--</p>
              <div id="locationName" class="small" style="font-weight:600"></div>
              <div class="meta" id="meta"></div>
            </div>
          </div>
        </div>
      </div>

    </section>

    <aside class="right">
      <div class="card">
        <h3 style="margin-top:0">Details</h3>
        <div class="stats" id="details">
          <div class="stat-row"><div>Feels like</div><div id="feels">--</div></div>
          <div class="stat-row"><div>Humidity</div><div id="humidity">--</div></div>
          <div class="stat-row"><div>Wind</div><div id="wind">--</div></div>
          <div class="stat-row"><div>Pressure</div><div id="pressure">--</div></div>
          <div class="stat-row"><div>Local time</div><div id="localtime">--</div></div>
          <div class="stat-row"><div>Sunrise / Sunset</div><div id="sun">--</div></div>
        </div>
      </div>

      <div style="height:14px"></div>
      <div class="card small"> Replace <code>YOUR_API_KEY</code> with your OpenWeatherMap API key.</div>
    </aside>

    <div class="footer">Made with ❤️ • OpenWeatherMap</div>
  </div>

  <script>
    // ---------- CONFIG ----------
    // Get an API key from https://openweathermap.org/ and paste here.
    const API_KEY = 'YOUR_API_KEY'; // <- REPLACE THIS
    // ----------------------------

    const $ = id => document.getElementById(id);
    const searchBtn = $('searchBtn'), locBtn = $('locBtn'), cityInput = $('cityInput');
    const unitSelect = $('unitSelect');

    const loading = $('loading'), panel = $('weatherPanel');
    const icon = $('icon'), temp = $('temp'), condition = $('condition'), locationName = $('locationName');
    const meta = $('meta');
    const feels = $('feels'), humidity = $('humidity'), wind = $('wind'), pressure = $('pressure'), localtime = $('localtime'), sun = $('sun');

    async function fetchWeatherByCity(q, units='metric'){
      showLoading('Fetching weather...');
      try{
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(q)}&units=${units}&appid=${API_KEY}`;
        const res = await fetch(url);
        if(!res.ok) throw new Error('Location not found');
        const data = await res.json();
        renderWeather(data, units);
      }catch(err){
        showError(err.message);
      }
    }

    async function fetchWeatherByCoords(lat, lon, units='metric'){
      showLoading('Fetching weather for your location...');
      try{
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=${units}&appid=${API_KEY}`;
        const res = await fetch(url);
        if(!res.ok) throw new Error('Failed to fetch weather for coordinates');
        const data = await res.json();
        renderWeather(data, units);
      }catch(err){
        showError(err.message);
      }
    }

    function showLoading(text){loading.style.display='block';loading.textContent=text;panel.style.display='none'}
    function showError(text){loading.style.display='block';loading.textContent='Error: '+text;panel.style.display='none'}

    function renderWeather(data, units){
      loading.style.display='none';panel.style.display='block';
      const w = data.weather && data.weather[0] ? data.weather[0] : {};
      const iconCode = w.icon || '';
      icon.src = iconCode ? `https://openweathermap.org/img/wn/${iconCode}@2x.png` : '';
      icon.alt = w.description || 'weather';

      temp.textContent = Math.round(data.main.temp) + (units==='metric' ? '°C' : '°F');
      condition.textContent = w.main ? `${w.main} — ${capitalize(w.description||'')}` : capitalize(w.description||'');
      locationName.textContent = `${data.name}, ${data.sys && data.sys.country ? data.sys.country : ''}`;

      // meta pills
      meta.innerHTML = '';
      addMeta(`${data.weather[0].main || ''}`);
      addMeta(`${data.visibility ? Math.round(data.visibility/1000)+' km visibility' : ''}`);
      addMeta(`${data.coord.lat.toFixed(2)}, ${data.coord.lon.toFixed(2)}`);

      // details
      feels.textContent = Math.round(data.main.feels_like) + (units==='metric' ? '°C' : '°F');
      humidity.textContent = data.main.humidity + '%';
      wind.textContent = (data.wind.speed ? data.wind.speed + (units==='metric' ? ' m/s' : ' mph') : '--');
      pressure.textContent = data.main.pressure + ' hPa';

      // local time using timezone offset returned by API (seconds)
      const tzOffset = data.timezone || 0; // seconds
      const local = new Date((Date.now()) + tzOffset*1000 - (new Date().getTimezoneOffset()*60000));
      localtime.textContent = local.toLocaleString();

      // sunrise/sunset
      if(data.sys && data.sys.sunrise && data.sys.sunset){
        const sr = new Date((data.sys.sunrise + tzOffset - (new Date().getTimezoneOffset()*60))*1000);
        const ss = new Date((data.sys.sunset + tzOffset - (new Date().getTimezoneOffset()*60))*1000);
        sun.textContent = `${sr.toLocaleTimeString()} / ${ss.toLocaleTimeString()}`;
      }
    }

    function addMeta(txt){ if(!txt) return; const d=document.createElement('div'); d.className='item'; d.textContent=txt; meta.appendChild(d); }
    function capitalize(s){ return s ? s.charAt(0).toUpperCase()+s.slice(1) : s }

    // Events
    searchBtn.addEventListener('click', ()=>{
      const q = cityInput.value.trim();
      if(!q) { showError('Please enter a city'); return }
      fetchWeatherByCity(q, unitSelect.value);
    });

    cityInput.addEventListener('keydown', e=>{ if(e.key==='Enter') searchBtn.click(); });

    locBtn.addEventListener('click', ()=>{
      if(!navigator.geolocation){ showError('Geolocation not supported'); return }
      showLoading('Getting your location...');
      navigator.geolocation.getCurrentPosition(pos=>{
        fetchWeatherByCoords(pos.coords.latitude, pos.coords.longitude, unitSelect.value);
      }, err=>{
        showError('Permission denied or unable to get location');
      }, {timeout:10000});
    });

    unitSelect.addEventListener('change', ()=>{
      // if there is currently displayed location, re-fetch in new units
      if(panel.style.display==='block' && locationName.textContent){
        const loc = locationName.textContent.split(',')[0];
        // try to use last coord if available (we'll store lastData)
        if(window.__lastWeather && window.__lastWeather.coord){
          fetchWeatherByCoords(window.__lastWeather.coord.lat, window.__lastWeather.coord.lon, unitSelect.value);
        } else if(loc) fetchWeatherByCity(loc, unitSelect.value);
      }
    });

    // Save last data for unit toggling
    function interceptRender(data, units){ window.__lastWeather = data; renderWeather(data, units); }

    // Small improvement: wrap renderWeather so we also store last data
    const originalRender = renderWeather;
    renderWeather = function(data, units){ window.__lastWeather = data; originalRender(data, units); };

    // If user included ?q=City in URL, auto-search
    (function autoSearchFromQuery(){
      try{
        const params = new URLSearchParams(location.search);
        const q = params.get('q');
        if(q){ cityInput.value = q; fetchWeatherByCity(q, unitSelect.value); }
      }catch(e){}
    })();

    // Helpful check before first fetch
    if(API_KEY === 'd40f33d92bff70a107d956b7931e10fc'){
      showLoading('Replace YOUR_API_KEY with a valid OpenWeatherMap API key in the code.');
    }
  </script>
</body>
</html>
