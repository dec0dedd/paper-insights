document.getElementById('uploadForm').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const fileInput = document.getElementById('fileInput');
    const fileName = fileInput.files[0].name;
    try {
      const res = await fetch('/upload', { method: 'POST', body: formData });
      const data = await res.json();
      const trace = {
        x: data.map(p => p.x),
        y: data.map(p => p.y),
        text: data.map(p => `PMID: ${p.pmid}<br>GSE: ${p.gse_id}<br>${p.title}`),
        mode: 'markers',
        marker: { size: 12, color: data.map(p => p.label), colorscale: 'Viridis' },
        type: 'scatter'
      };
      const layout = {
        title: `Chart for ${fileName}`,
        margin: { t: 50 }
      };
      Plotly.newPlot('plot', [trace], layout);
    } catch (err) {
      console.error('Error during file upload or plotting:', err);
    }
  }
