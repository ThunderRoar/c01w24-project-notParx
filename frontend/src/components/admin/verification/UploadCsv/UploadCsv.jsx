import React, { useState, useRef } from 'react';
import './UploadCsv.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import UploadFileIcon from '@mui/icons-material/UploadFile';

const UploadCsv = ({ onClose }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const dropZoneRef = useRef(null);
    const fileInputRef = useRef(null);

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();

        const files = e.dataTransfer.files;
        if (files.length) {
            setSelectedFile(files[0]);
        }
    };

    return (
        <div className="upload-content">
            <div className="popup-header">
                <div>Upload CSVs for Verification</div>
                <HighlightOffIcon onClick={onClose} className='close-icon' />
            </div>
            <div className="upload-area">
                <div className="drop-zone"
                    ref={dropZoneRef}
                    onDragEnter={handleDragEnter}
                    onDragLeave={handleDragLeave}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}>
                    <UploadFileIcon className='upload-icon' />
                    <p>Drop your files here or <a className='direct-upload' href="#" onClick={(e) => fileInputRef.current.click()}>browse</a></p>
                    <input type="file" ref={fileInputRef} style={{ display: 'none' }} 
                        onChange={(event) => setSelectedFile(event.target.files[0])} />
                </div>
            </div>
            <div className='controls'>
                <button className="verify-button">Verify</button>
            </div>
        </div>
    );
};

export default UploadCsv;
