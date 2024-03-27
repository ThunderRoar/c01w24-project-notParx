import React, { useState, useRef, useCallback, useLayoutEffect } from 'react';
import './UploadCsv.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { FiLoader } from "react-icons/fi";

const UploadCsv = ({ onClose }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [mongoID, setMongoID] = useState('');
    const [fileError, setFileError] = useState(false);
    const [noFileError, setNoFileError] = useState(false);
    const [uploadError, setUploadError] = useState(false);
    const [loading, setLoading] = useState(false);

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
        setFileError(false);
        setUploadError(false);
        setNoFileError(false);
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
                setFileError(true);
            }
        }
    };

    const handleVerfiy = async () => {
        setFileError(false);
        setUploadError(false);
        setNoFileError(false);
        setLoading(true);
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
                    onClose();
                } else {
                    console.log("Error uploading file: ", response.statusText);
                    setUploadError(true);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error('Error uploading file: ', err);
                setUploadError(true);
                setLoading(false);
            });
        } else {
            setErrorMessage("Please upload a CSV file first...");
            setNoFileError(true);
        }
        setLoading(false);
    }

    const handleFileSelected = (event) => {
        setNoFileError(false);
        setFileError(false);
        setUploadError(false);
        setErrorMessage('');
        setSelectedFile(event.target.files[0])
    }

    return (
        <div className="upload-content">
            <div className="popup-header">
                <div>Upload CSVs for Verification</div>
                <HighlightOffIcon onClick={onClose} className='close-icon' />
            </div>
            {fileError && (
                    <div className='error-popup'>Incorrect file type. Please use a .csv file</div>
            )}
            {noFileError && (
                    <div className='error-popup'>No file selected. Please upload a file</div>
            )}
            {uploadError && (
                    <div className='error-popup'>Something went wrong. Please try again</div>
            )}
            <div className="upload-area">
                <div className='drop-zone'
                    ref={dropZoneRef}
                    onDragEnter={handleDragEnter}
                    onDragLeave={handleDragLeave}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    style={{ background: errorMessage ? '#ffcccc' : '#F1FAEF' }}>
                    <UploadFileIcon className='upload-icon' />
                    { selectedFile && (
                        <>
                            <p>Uploaded file: {selectedFile.name}</p>
                            <p>Drop or <a className='direct-upload' href="#" onClick={(e) => fileInputRef.current.click()}>select</a> a different file</p>
                        </>
                    )}
                    { !selectedFile && (
                        errorMessage 
                        ? <p>Please <a className='direct-upload' href="#" onClick={(e) => fileInputRef.current.click()}>upload</a> a CSV file first...</p>
                        : <p>Drop your files here or <a className='direct-upload' href="#" onClick={(e) => fileInputRef.current.click()}>browse</a></p>
                    )}
                    <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept='.csv'
                        onChange={handleFileSelected} />
                </div>
            </div>
            <div className='controls'>
            {!loading && (
                    <button className="verify-button" onClick={handleVerfiy}>Verify</button>
            )}
            {loading && (
                 <div className='loading-button'>
                    <FiLoader></FiLoader>
                 </div>
            )}
            </div>

        </div>
    );
};

export default UploadCsv;
