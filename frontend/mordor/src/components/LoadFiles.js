import React, { useEffect } from 'react';
import { useState } from 'react';

const URL = "http://localhost:3000/"

function LoadFiles(props) {
    const [hiddenFiles, setHiddenFiles] = useState([]);
    const [hiddenDirectories, setHiddenDirectories] = useState([]);
    const [files, setFiles] = useState([]);
    const [directories, setDirectories] = useState([]);
    const [path, setPath] = useState("");

    function fetchFiles() {
        fetch("http://127.0.0.1:8000/list" + window.location.pathname)
            .then(response => response.json())
            .then(result => {
                setHiddenFiles(result.hidden_files);
                setHiddenDirectories(result.hidden_directories);
                setFiles(result.files);
                setDirectories(result.directories);
                setPath(result.path);
                console.log(result)
            })
            .catch(error => console.log('error', error));
    }
    
    useEffect(() => {
        console.log(path)
        fetchFiles();
    }, [path]
    );
    
    return <div>
        {hiddenFiles.map(file => <a href={URL + path + file}><h3 key={file}>{file}</h3></a>)}
        {hiddenDirectories.map(file => <a href={URL + path + file}><h3 key={file}>{file}</h3></a>)}
        {files.map(file => <a href={URL + path + file}><h3 key={file}>{file}</h3></a>)}
        {directories.map(file => <a href={URL + path + file}><h3 key={file}>{file}</h3></a>)}
    </div>
}

export default LoadFiles;
