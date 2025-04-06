document.getElementById('uploadForm').onsubmit = async function(e) {
  e.preventDefault()
  const formData = new FormData(this);
  const fileName = document.getElementById('fileInput').files[0].name;

  try {
    const res = await fetch('/upload', {method: 'POST', body: formData});
    const data = await res.json();

    const trace = {
      x: data.map(p => p.x),
      y: data.map(p => p.y),
      text: data.map(p => `PMID: ${p.pmid}<br>GSE: ${p.gse_id}<br>${p.title}`),
      mode: 'markers',
      marker: { 
        size: 10,
        color: data.map(p => p.label),
        colorscale: 'Viridis'
      },
      type: 'scatter'
    };

    const layout = {
      title: `Chart for ${fileName}`,
      autosize: true,
      margin: {
        t: 50
      }
    };

    const config = { responsive: true };
    Plotly.newPlot('plot', [trace], layout, config);
  } catch (err) {
    console.error('Error during file upload or plotting:', err);
  }
}
