import { useDropzone } from "react-dropzone";
import { useState, useCallback } from "react";
import "../styles/Uploader.css";

export default function Uploader({ onFile }) {
  const [state, setState] = useState("circle"); // 'circle' | 'expanded' | 'uploaded'

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFile(acceptedFiles[0]);
      setState("uploaded");
      setTimeout(() => setState("circle"), 2000); // revert to circle after 2s
    }
  }, [onFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    noClick: state === "circle",
    noKeyboard: true,
  });

  return (
    <div
      {...getRootProps({
        className: `dropzone ${state} ${isDragActive ? "drag-active" : ""}`,
        onClick: () => {
          if (state === "circle") setState("expanded");
        },
      })}
    >
      <input {...getInputProps()} />
      {state === "circle" && <span className="plus-sign">+</span>}
      {state === "expanded" && (
        <>
          <p>Drag & drop a data file, or click to select</p>
          <ul className="file-list">
            <li>Excel (.xls/.xlsx)</li>
            <li>CSV</li>
            <li>PDF (tables)</li>
            <li>Access (.accdb/.mdb)</li>
          </ul>
        </>
      )}
      {state === "uploaded" && <span className="plus-sign">✓</span>}
    </div>
  );
}




