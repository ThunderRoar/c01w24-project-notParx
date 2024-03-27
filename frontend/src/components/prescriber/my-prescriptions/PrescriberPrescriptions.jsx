import './PrescriberPrescriptions.scss';
import PrescriberAddPrescription from './PrescriberAddPrescription/PrescriberAddPrescription';
import decodeToken from '../../../token_handling/tokenHandling';

import * as React from 'react';
import ReactPopup from 'reactjs-popup';
import { Button } from '@mui/material';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

const PrescriberPrescriptions = () => {
    const prescriptionColumns = [ // Sample columns - add depending on what api returns
        { id: 'prescriberCode', label: 'Provider Code' },
        { id: 'patientInitials', label: 'Patient Initials' },
        { id: 'dateOfPrescription', label: 'Date' },
        { id: 'discoveryPassPrescribed', label: 'Discovery Pass' },
        { id: 'matchedPatient', label: 'Matched Patient' },
        { id: 'prescriberStatus', label: 'Status' },
        // { id: 'pdf', label: 'Prescription PDF' },
    ];

    const [prescriptionPage, setPrescriptionPage] = React.useState(0);
    const [prescriptionRowsPerPage, setPrescriptionRowsPerPage] = React.useState(5); 
    const [showPopup, setShowPopup] = React.useState(false);
    const [prescriptionDBdata, setPrescriptionDBdata] = React.useState([]);

    const handlePrescriptionPageChange = (event, newPage) => {
        setPrescriptionPage(newPage);
    };

    const handlePrescriptionRowsPerPageChange = (event) => {
        setPrescriptionRowsPerPage(+event.target.value);
        setPrescriptionPage(0); 
    };

    const handleAddPresClick = () => {
        setShowPopup(true);  // Open the popup
    };

    const handlePopupClose = () => {
        setShowPopup(false); // Close the popup
    };

    React.useEffect(() => {
        const handleGetPrescriptions = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const decodedToken = decodeToken(token);
                    const prescriberCode = decodedToken.username;
                    console.log(prescriberCode);

                    await fetch('https://notparx-prescription-service.azurewebsites.net/api/prescriberPrescriptions/' + prescriberCode + '/', {
                        method: 'GET',
                    })
                    .then (async response => {
                        if (response.ok) {
                            let data = await response.json();
                            console.log(data);
                            for (let p of data) {
                                p["patientInitials"] = p["prescriptionID"].slice(-2);
                                p["discoveryPassPrescribed"] = p["discoveryPassPrescribed"] ? "Prescribed" : "N/A";
                            }
                            setPrescriptionDBdata(data);
                        } else {
                            console.error('Error fetching prescriptions: ', response.statusText);
                        }
                    })
                } else {
                    console.error('User not logged in');
                }
            } catch(error) {
                console.error('Error fetching prescription: ', error);
            }
        };

        handleGetPrescriptions();
    }, [])

    // TODO: connect backend endpoint here to download prescription
    const handleDownloadPrescription = async (prescriptionID) => {
        url = 'https://notparx-prescription-service.azurewebsites.net/api/downloadprescription/' + prescriptionID + '/';
        try {
            const response = await fetch(url, {
                method: 'GET',
                // Add headers if needed, e.g., Authorization for protected routes
            });        
            if (!response.ok) {
                console.error('Error downloading prescription: ', response.statusText);
            }

            const cdHeader = response.headers.get('content-disposition');
            let filename = "prescription.pdf";
            if (cdHeader) {
                const matches = /filename="([^"]+)"/.exec(cdHeader);
                if (matches && matches.length > 1) {
                    filename = matches[1];
                }
            }
            // Process the response as a Blob to handle the binary PDF data
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', filename); // Set the file name for the download
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        }
        catch (error) {
            console.error('Download error:', error);
            // Handle error scenario, e.g., show a notification or message to the user
        }
    }

    return (
        <div className='prescriber-prescriptions-component'>
            <div className='page-header'>
                <span>My Prescriptions</span>
            </div>
            <div className='content'>
                <div className='controls'>
                    <Button className='add-new-btn' onClick={handleAddPresClick}>Add New</Button>
                </div>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                <TableRow className='header-row'>
                                    {prescriptionColumns.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}
                                    <TableCell key={"prescriptionButton"}><span>Prescription PDF</span></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {prescriptionDBdata.slice(prescriptionPage * prescriptionRowsPerPage,
                                    prescriptionPage * prescriptionRowsPerPage + prescriptionRowsPerPage).map((row, id) => (
                                    <TableRow className='table-row' key={id}>
                                        {/* Render prescription columns */}
                                        {prescriptionColumns.map((column) => (
                                            <TableCell key={column.id}>{row[column.id]}</TableCell>
                                        ))}
                                        <TableCell key="prescriptionButton"> 
                                            {/* TODO: handle view prescriptions */}
                                            <Button className='btn' onClick={() => handleDownloadPrescription(row["prescriptionID"])}>
                                                <span>View Prescription</span>
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25]}
                        component="div"
                        count={prescriptionDBdata.length} 
                        rowsPerPage={prescriptionRowsPerPage}
                        page={prescriptionPage}
                        onPageChange={handlePrescriptionPageChange}
                        onRowsPerPageChange={handlePrescriptionRowsPerPageChange}
                    />
                </div>
            </div>
            <ReactPopup open={showPopup} closeOnDocumentClick={false} onClose={handlePopupClose}>
                <PrescriberAddPrescription onClose={handlePopupClose} /> 
            </ReactPopup>
        </div>
    );
};

export default PrescriberPrescriptions;
