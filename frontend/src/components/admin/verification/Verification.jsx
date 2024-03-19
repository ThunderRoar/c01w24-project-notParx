import './Verification.scss';
import { Button } from '@mui/material';
import * as React from 'react';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import UploadCsv from './UploadCsv/UploadCsv';
import ReactPopup from 'reactjs-popup';
import axios from 'axios';

const Verification = () => {

    const [rowsPerPage, setRowsPerPage] = React.useState(5); 
    const [page, setPage] = React.useState(0);
    const [files, setFiles] = React.useState([]);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0); // Reset page to 0 when rows per page change
    };

    React.useEffect(() => {
        const getFiles = async () => {
            axios.get("https://notparx-prescriber-service.azurewebsites.net/api/files/")
                .then(res => {
                    const flist = res.data;
                    const newFiles = [];
                    for (let f of flist) {
                        const file = {
                            name: f["file_name"],
                            date: f["date_uploaded"],
                            status: f["current_status"] === "Uploaded" ? "Processed" : f["current_status"] ,
                            _id: f["_id"]
                        };
                        newFiles.push(file);
                    }
                    setFiles(newFiles);
                })
                .catch(err => {
                    console.error('Error fetching file list: ', err);
                });
        };
        
        getFiles();

        return () => {
            setFiles([]);
        };
    }, []);
    
    // const sampleData = [
    //     { id: 1, name: 'Item 1', date: '14 Feb 2024', status: 'Complete', download: true },
    //     { id: 2, name: 'Item 2', date: '15 Feb 2024', status: 'Failed', download: true },
    //     { id: 3, name: 'Item 3', date: '16 Feb 2024', status: 'In Progress', download: false },
    // ];
    
    const columns = [
        { id: 'name', label: 'Name' },
        { id: 'date', label: 'Date Uploaded' },
        { id: 'status', label: 'Status' },
    ];

    const [showPopup, setShowPopup] = React.useState(false);

    const handleUploadClick = () => {
        setShowPopup(true);  // Open the popup
    };

    const handlePopupClose = () => {
        setShowPopup(false); // Close the popup
    };

    // Download a particular CSV file from a row
    const handleDownloadCSV = (fileId, originalName) => {
        axios.get("https://notparx-prescriber-service.azurewebsites.net/api/download/" + fileId)
                .then(res => {
                    if (res.status === 200) {
                        const data = res.data;
                        console.log(data["download_url"]);

                        // Download file from azure URL and force browser to save it to downloads.
                        fetch(data["download_url"], {method: 'GET'}).then(res2 =>
                            res2.blob()).then( blob => {
                                const url = window.URL.createObjectURL(
                                    new Blob([blob]),
                                );
                                // Create a temporary link elem, click it, and cleanup
                                const link = document.createElement('a');
                                link.href = url;
                                link.setAttribute(
                                    'download',
                                    originalName,
                                );
                                document.body.appendChild(link);
                                link.click();
                                link.parentNode.removeChild(link);
                            })
                    }
                    else {
                        console.error('Error fetching file: ', res.statusText);
                    }
                })
                .catch(err => {
                    console.error('Error fetching file: ', err);
                });
    }

    return (
        <div className='admin-verification-component'>
            <div className='verif-header'> Your CSVs </div>
            <div className='content'>
                <div className='controls'>
                    <Button className='upload-button' onClick={handleUploadClick}>
                        <span>Upload CSV</span>
                    </Button>
                </div>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                <TableRow className='header-row'>
                                    {columns.map((column) => (
                                    <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}
                                    <TableCell key={"downloadButton"}></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {files.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, id) => (
                                    <TableRow className='table-row' key={id}>
                                        {columns.map((column) => (
                                            <TableCell key={column.id}>{row[column.id]}</TableCell>
                                        ))}
                                        <TableCell key={"downloadButton"}>
                                        <Button className='upload-button' onClick={() => handleDownloadCSV(row["_id"], row["name"])}>
                                            <span>Download CSV</span>
                                        </Button>
                                        </TableCell>

                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25]} // Options for rows per page
                        component="div"
                        count={files.length} 
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </div>
            </div>
            <ReactPopup open={showPopup} closeOnDocumentClick={true} onClose={handlePopupClose}>
                <UploadCsv onClose={handlePopupClose} /> 
            </ReactPopup>
        </div>
    );
};

export default Verification;