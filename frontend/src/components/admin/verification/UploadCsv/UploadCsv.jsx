import React, { useState, useRef, useCallback, useLayoutEffect } from 'react';
import './UploadCsv.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { useDropzone } from 'react-dropzone';
import PropTypes from 'prop-types';
import { responsiveProperty } from '@mui/material/styles/cssUtils';

const UploadCsv = ({ onClose }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [mongoID, setMongoID] = useState('');

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
        if (files && files.length) {
            const file = files[0];
            if (file.name.endsWith(".csv")) {
                setSelectedFile(file);
                setErrorMessage('');
            } else {
                // alert('Please drop a valid Excel file.');
                setErrorMessage("Please drop a valid CSV file.");
            }
        }
    };

    const handleVerfiy = async () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            await fetch('https://notparx-prescriber-service.azurewebsites.net/api/upload/', {
                method: 'POST', 
                body: formData,
            })
            .then (async response => {
                if (response.ok) {
                    let { mongoid } = await response.json();
                    console.log("File uploaded successfully.");
                    // console.log(mongoid);
                    setMongoID(mongoid);
                } else {
                    console.log("Error uploading file: ", response.statusText);
                }
            })
            .catch(err => {
                console.error('Error uploading file: ', err);
            });
        } else {
            setErrorMessage("Please upload a CSV file first...");
        }
    }

    return (
        <div className="upload-content">
            <div className="popup-header">
                <div>Upload CSVs for Verification</div>
                <HighlightOffIcon onClick={onClose} className='close-icon' />
            </div>
            <div className="upload-area">
                <div className='drop-zone'
                    ref={dropZoneRef}
                    onDragEnter={handleDragEnter}
                    onDragLeave={handleDragLeave}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    style={{ background: errorMessage ? '#ffcccc' : '#F1FAEF' }}>
                    <UploadFileIcon className='upload-icon' />
                    { errorMessage ? <p>{errorMessage}</p> : <p>Drop your files here or <a className='direct-upload' href="#" onClick={(e) => fileInputRef.current.click()}>browse</a></p>}
                    <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept='.csv'
                        onChange={(event) => setSelectedFile(event.target.files[0])} />
                </div>
            </div>
            <div className='controls'>
                <button className="verify-button" onClick={handleVerfiy}>Verify</button>
                {selectedFile && <p>Uploaded file: {selectedFile.name}</p>}
            </div>
        </div>
    );
};

export default UploadCsv;
