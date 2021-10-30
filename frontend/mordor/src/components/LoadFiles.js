import React, { useEffect } from 'react';
import { useState } from 'react';

function LoadFiles(props) {
    const [hiddenFiles, setHiddenFiles] = useState([])
    const [hiddenDirectories, setHiddenDirectories] = useState([])
    const [files, setFiles] = useState([])
    const [directories, setDirectories] = useState([])

    
    function fetchFiles() {
        fetch("http://127.0.0.1:8000/list/")
            .then(response => response.json())
            .then(result => {
                setHiddenFiles(result.hidden_files)
                setHiddenDirectories(result.hidden_directories)
                setFiles(result.files)
                setDirectories(result.directories)
            })
            .catch(error => console.log('error', error));
    }
    
    useEffect(() => {
        fetchFiles()
    })
    
    return <div>
        {hiddenFiles.map(file => <h1 key={file}>{file}</h1>)}
        {hiddenDirectories.map(file => <h1 key={file}>{file}</h1>)}
        {files.map(file => <h1 key={file}>{file}</h1>)}
        {directories.map(file => <h1 key={file}>{file}</h1>)}
    </div>
}

export default LoadFiles