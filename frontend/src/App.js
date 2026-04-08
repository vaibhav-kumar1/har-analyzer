import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState({});

  const upload = async () => {
    const fd = new FormData();
    fd.append("file", file);

    const res = await axios.post(`${process.env.REACT_APP_API_URL}/analyze`, fd);
    setData(res.data);
  };

  const downloadFile = (content, filename) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>🔥 HAR Analyzer PRO</h1>

      <input type="file" onChange={(e)=>setFile(e.target.files[0])}/>
      <button onClick={upload}>Analyze</button>

      {/* ================= TABLE ================= */}
      <h2>📊 Requests</h2>
      <div style={{ maxHeight: 300, overflow: "auto", border: "1px solid #ccc" }}>
        <table width="100%">
          <thead>
            <tr>
              <th>#</th><th>Method</th><th>URL</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.entries?.map((e,i)=>(
              <tr key={i}>
                <td>{i}</td>
                <td>{e.method}</td>
                <td style={{ wordBreak: "break-all" }}>{e.url}</td>
                <td>{e.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ================= CORRELATION ================= */}
      <h2>🔗 Correlation</h2>
      <ul>
        {data.correlations?.map((c,i)=>(
          <li key={i}>
            {c.source} ➝ {c.target} | {c.variable}
          </li>
        ))}
      </ul>

      {/* ================= GRAPH ================= */}
      <h2>📊 Correlation Graph</h2>
      <div style={{ border: "1px solid black", padding: 10 }}>
        {data.correlations?.map((c,i)=>(
          <div key={i}>
            🔵 Step {c.source} ➝ 🟢 Step {c.target}
          </div>
        ))}
      </div>

      {/* ================= DOWNLOAD ================= */}
      <h2>⬇️ Download Scripts</h2>

      <button onClick={()=>downloadFile(data.jmeter,"test.jmx")}>
        Download JMeter
      </button>

      <button onClick={()=>downloadFile(data.loadrunner,"script.c")}>
        Download LoadRunner
      </button>

      <button onClick={()=>downloadFile(data.k6,"script.js")}>
        Download k6
      </button>

      {/* ================= AI ================= */}
      <h2>🤖 AI</h2>
      <pre style={{ background: "#eee", padding: 10 }}>
        {JSON.stringify(data.ai,null,2)}
      </pre>
    </div>
  );
}

export default App;